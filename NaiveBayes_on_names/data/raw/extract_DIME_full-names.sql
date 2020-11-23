with 
cand as (select distinct name as raw ,
                         fname,
                         ffname,
                         mname,
                         nname,
                         lname,
                         'cand' as sourcetable
         from "candDB"),     --176.777 dist 92088
contrib as (select distinct contributor_name as raw,
                            contributor_fname as fname,
                            contributor_ffname as ffname ,
                            contributor_mname as mname,
                            '' as nname,
                            contributor_lname as lname,
                            'contrib' as sourcetable
            from "contribDB" 
            where contributor_type='I'), -- 122.637.975 dist 15.621.109
donor as (select distinct most_recent_contributor_name as raw,
                 '' as fname,
                 '' as ffname,
                 '' as mname,
                 '' as nname,
                 '' as lname,
                 'donor' as sourcetable
          from "donorDB"
          where contributor_type='I'), -- 14.694.491 dist 9.858.677
unionall as ( select * from cand UNION ALL
              select * from contrib UNION ALL
              select * from donor
              )
select * from unionall   --25.571.895
;
