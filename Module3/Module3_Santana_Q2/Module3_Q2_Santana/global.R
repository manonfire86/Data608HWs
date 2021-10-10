library(shiny)
library(plotly)
library(dplyr)
cdc_mort_df = read.csv('https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv', header= TRUE)
cdc_mort_df$Mortality_rate = (cdc_mort_df$Deaths/cdc_mort_df$Population)*100
cdc_mort_df = cdc_mort_df %>% select(ICD.Chapter,State,Year,Mortality_rate)
cdc_mort_df = cdc_mort_df %>% group_by(ICD.Chapter,State,Year) %>% summarise(Mortality_rate = sum(Mortality_rate))