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
    dataselect <- reactive({dataselect <- subset(filt_cdc_mort_df, ICD.Chapter==input$cause)})
    output$plot1 = renderPlotly({
        plot_ly(dataselect(),x=~reorder(ICD.Chapter,Crude.Rate),y=~Crude.Rate,color=~State,type="bar")%>% layout(title = '2010 Mortality Rate (CDC)')
    })
})
