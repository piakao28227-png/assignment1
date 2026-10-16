"""Convert LaTeX to editable Word OMML using Pandoc, with a persistent local cache."""
from pathlib import Path
from copy import deepcopy
import hashlib, subprocess, zipfile
from lxml import etree
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

CACHE=Path('/workspace/assignment1-render/math-cache')
CACHE.mkdir(parents=True,exist_ok=True)
NS={'m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}

def omml(latex,display=False):
 for label in ['CAC','LTV','TCO','PV','E','G','e']:
  latex=latex.replace('\\mathrm{'+label+'}','\\text{'+label+'}')
 key=hashlib.sha256((str(display)+latex).encode()).hexdigest()
 path=CACHE/(key+'.docx')
 if not path.exists():
  delim='$$' if display else '$'
  subprocess.run(['pandoc','-f','markdown+tex_math_dollars','-t','docx','-o',str(path)],input=f'{delim}{latex}{delim}\n',text=True,check=True,capture_output=True)
 with zipfile.ZipFile(path) as z:root=etree.fromstring(z.read('word/document.xml'))
 node=root.find('.//m:oMath',NS)
 if node is None:raise ValueError('Pandoc did not create OMML: '+latex)
 node=deepcopy(node)
 # Use an installed OpenType math font for PDF export and Word editing.
 for run in node.findall('.//m:r',NS):
  props=run.find(qn('w:rPr'))
  if props is None:
   props=OxmlElement('w:rPr')
   run.insert(1 if len(run) and run[0].tag==qn('m:rPr') else 0,props)
  fonts=OxmlElement('w:rFonts')
  fontname='Latin Modern Roman' if run.find('m:rPr/m:nor',NS) is not None else 'Latin Modern Math'
  for name in ['ascii','hAnsi','eastAsia','cs']:fonts.set(qn('w:'+name),fontname)
  props.append(fonts)
  mathstyle=run.find('m:rPr/m:sty',NS)
  if mathstyle is not None and mathstyle.get(qn('m:val'))=='p':
   italic=OxmlElement('w:i');italic.set(qn('w:val'),'0');props.append(italic)
  size=OxmlElement('w:sz');size.set(qn('w:val'),'22');props.append(size)
 return node
