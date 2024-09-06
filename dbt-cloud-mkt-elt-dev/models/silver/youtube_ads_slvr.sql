SELECT *,
upper(
  concat(
    replace(Company," ",""),"_",
    case
      when Campaign_Type = 'Email' then 'EM'
      when Campaign_Type = 'Influencer' then 'INF'
      when Campaign_Type = 'Display' then 'DSP'
      when Campaign_Type = 'Search' then 'SRCH'
      when Campaign_Type = 'Social Media' then 'SM'
      end, '_',
      replace(replace(replace(Target_Audience, 'Woman','W-'),'Men', 'M-'), 'All Ages', 'A-A'),'_',
      case
        when Location =  'New York' then 'NY'
        when Location =  'Miami' then 'MIA'
        when Location =  'Boston' then 'BOS'
        when Location =  'Chicago' then 'CHI'
        when Location =  'Seattle' then 'SEA'
        when Location =  'Las Vegas' then 'LV'
        when Location =  'Washington' then 'WDC'
        when Location =  'Nueva Orleans' then 'NO'
        when Location =  'San Francisco' then 'SF'
        when Location =  'Los Angeles' then 'LA'
        end
  )
) as Campaign_Name,
DATE_ADD(Date, INTERVAL cast(replace(Duration, 'days', '')as INT64)DAY) as Date_End
from {{source("raw","youtube_ads_raw")}}