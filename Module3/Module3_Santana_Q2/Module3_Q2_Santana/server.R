#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#



# Define server logic required to draw a histogram
shinyServer(function(input, output) {
    dataselect <- reactive({dataselect <- subset(cdc_mort_df, ICD.Chapter==input$cause & State==input$State)})
    output$plot1 = renderPlotly({
        plot_ly(dataselect(),x=~Year,y=~Mortality_rate,type="scatter",mode='lines') %>% layout(title = 'Mortality Rate Trends: State and Cause')
    })
})
