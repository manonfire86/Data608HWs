#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#


# Define UI for application that draws a histogram
shinyUI(fluidPage(
    
    # Application title
    headerPanel("Mortality Rate Trends: State and Cause"),
    
    # Dynamic Row
    selectInput("cause", "Causes of Death:", 
                choices=sort(unique(cdc_mort_df$ICD.Chapter))),
    selectInput("State", "Specific State:", 
                choices=sort(unique(cdc_mort_df$State))),
    
    mainPanel(plotlyOutput('plot1'))
    
))
