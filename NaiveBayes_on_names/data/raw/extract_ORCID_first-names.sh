orig_pwd=`pwd`

for i in `ls -d ORCID_2020_10_summaries/*`
do


cd $i
fgrep '<personal-details:given-names>' *xml | sed 's/<personal-details:given-names>//g' | sed 's#</personal-details:given-names>##g' 

#fgrep '<personal-details:family-name>' *xml | sed 's/<personal-details:family-name>//g' | sed 's#</personal-details:family-name>##g'

cd $orig_pwd
done



