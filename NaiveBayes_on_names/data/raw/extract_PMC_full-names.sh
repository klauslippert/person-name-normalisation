for i in $(find folder_*.xml.tar.gz -name *nxml)
do
  python3 extract_PMC_full-names.py $i
done
