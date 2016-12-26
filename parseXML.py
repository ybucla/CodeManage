from xml.dom.minidom import parse 
import xml.dom.minidom
import re

def main(xmlfile):
	DOMTree = xml.dom.minidom.parse(xmlfile) 
	Data = DOMTree.documentElement 

	for SpectrumIdentificationResult in Data.getElementsByTagName('SpectrumIdentificationResult'):
		SpectrumIdentificationItems = SpectrumIdentificationResult.getElementsByTagName('SpectrumIdentificationItem')
		peptide_ref = ''
		experimentalMassToCharge = ''
		for si in SpectrumIdentificationItems:
			peptide_ref = re.sub(re.compile('\|.*$'),'',si.getAttribute('peptide_ref'))
			experimentalMassToCharge = si.getAttribute('experimentalMassToCharge')

		searchEngineScore = ''
		cvParams = SpectrumIdentificationResult.getElementsByTagName('cvParam')	
		for cp in cvParams:
			searchEngineScore += cp.getAttribute('name')+'-'+cp.getAttribute('value')+';'
		
		PeptideEvidenceRefs = SpectrumIdentificationResult.getElementsByTagName('PeptideEvidenceRef')
		for pe in PeptideEvidenceRefs:
			id = re.sub(re.compile('\|.*$'),'',pe.getAttribute('peptideEvidence_ref'))
			print peptide_ref,"\t",id,"\t",searchEngineScore,"\t",experimentalMassToCharge

if __name__ == '__main__':
	main('TCGA-AG-A00H-01A-31_W_VU_20121008_A0218_4B_R_FR01.mzid')