import xml.etree.ElementTree as ET
import re,os,sys

def main(id,xmlfile):
	outdir = id
	if not os.path.exists(outdir):
		os.makedirs(outdir)
	outfile = outdir+'/'+os.path.basename(xmlfile).replace('xml','out')

	tree = ET.parse(xmlfile)
	root = tree.getroot()

	result = []
	index = 1
	Experiment = root.findall('Experiment')[0]

	idmzdict = {}
	spectrumList = Experiment.find('mzData').find('spectrumList')
	for spectrum in spectrumList.findall('spectrum'):
		sid = spectrum.get('id')
		ionSelection = spectrum.find('spectrumDesc').find('precursorList').find('precursor').find('ionSelection')
		for cvParam in ionSelection.findall('cvParam'):
			if cvParam.get('name') == 'selected ion m/z':idmzdict[sid] = cvParam.get('value')

	for TwoDimensionalIdentification in Experiment.findall('TwoDimensionalIdentification'):
		Accession = TwoDimensionalIdentification.find('Accession').text
		for PeptideItem in TwoDimensionalIdentification.findall('PeptideItem'):
			Sequence = PeptideItem.find('Sequence').text
			SpectrumReference = PeptideItem.find('SpectrumReference').text
			SEQUEST_Score = ''
			Delta_Cn = ''
			additional = PeptideItem.find('additional')
			for cvParam in additional.findall('cvParam'):
				if cvParam.get('name') == 'SEQUEST Score': SEQUEST_Score = cvParam.get('value')
				if cvParam.get('name') == 'Delta Cn': Delta_Cn = cvParam.get('value')
			result.append(str(index)+'\t'+Sequence+'\t'+Accession+'\t'+SEQUEST_Score+';'+Delta_Cn+'\t'+idmzdict[SpectrumReference])
			index += 1
	with open(outfile,'w') as fout:
		for r in result:
			fout.write(r+'\n')

if __name__ == '__main__':
	main('test','24063.xml')
