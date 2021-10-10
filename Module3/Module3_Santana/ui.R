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
    headerPanel("2010 Mortality Rate (CDC)"),
    
    # Dynamic Row
    selectInput("cause", "Causes of Death:", 
                         choices=sort(unique(cdc_mort_df[cdc_mort_df$Year==2010,]$ICD.Chapter))),

    mainPanel(plotlyOutput('plot1'))
    
))
