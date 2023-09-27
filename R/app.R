# Load libraries
library(shiny)
library(ggplot2)
library(fmsb)
library(plotly)

# Shiny UI part
ui <- fluidPage(
  titlePanel("YouTube Data Visualization"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("plot_type", "Select Chart Type:",
                  choices = c("Line Plot", "Pie Chart", "Density Plot")),
      uiOutput("x_axis_selector")
    ),
    
    mainPanel(
      plotOutput("selected_plot")
    )
  )
)

# Shiny server part
server <- function(input, output, session) {
  
  # Dynamically generate UI for X-axis selector.
  output$x_axis_selector <- renderUI({
    # Show different X-axis options based on chart type.
    switch(input$plot_type,
           "Line Plot" = {
             line_cols <- c("Rank", "Uploads", "Lowest Monthly Earnings", "Highest Monthly Earnings", "Subscribers For Last 30 Days", "Video Views For The Last 30 Days")
             selectInput("x_axis", "Select X-Axis:", choices = line_cols, selected = line_cols[1])
           },
           "Pie Chart" = {
             pie_cols <- c("Category", "Country", "Channel Type")
             selectInput("x_axis", "Select X-Axis:", choices = pie_cols, selected = pie_cols[1])
           },
           "Density Plot" = {
             density_cols <- c("Rank", "Subscribers", "Uploads", "Population", "Latitude", "Longitude")
             selectInput("x_axis", "Select X-Axis:", choices = density_cols, selected = density_cols[1])
           })
  })
  
  output$selected_plot <- renderPlot({
    req(input$x_axis, youtube) # Check inputs and datasets for availability.
    
    # Delete NA values.
    youtube <- na.omit(youtube[, c(input$x_axis), drop=FALSE])
    
    # Line Plot
    if (input$plot_type == "Line Plot") {
      if (input$x_axis %in% names(youtube)) {  # # Check for the existence of user-selected X-axis variables in the YouTube dataset.
        p <- ggplot(youtube, aes(x = 1:nrow(youtube))) +
          geom_line(aes(y = !!sym(input$x_axis)), color = "skyblue") +
          labs(title = paste("Linear analysis of Subscribers and", input$x_axis),
               x = input$x_axis, 
               y = "Subscribers") +
          theme_minimal() +
          theme(
            plot.title = element_text(face = "bold", hjust = 0.5, size = 16), 
            axis.title = element_text(size = 14),
            axis.text = element_text(size = 12)
          )
        
        print(p)
        return(p)
      }
    }
    
    # Pie Chart
    if (input$plot_type == "Pie Chart" && !is.null(input$x_axis)) {
      selected_data <- youtube[[input$x_axis]]
      if (is.character(selected_data) && !is.null(selected_data)) {
        selected_data <- na.omit(selected_data)
        category_counts <- table(selected_data)
        if (length(category_counts) > 0) {
          top_n <- 5
          category_counts_sorted <- sort(category_counts, decreasing = TRUE) # Sort the number of categories.
          
          # If there are more than 5 categories, the others are categorized as "Others".
          if (length(category_counts_sorted) > top_n) {
            other_count <- sum(category_counts_sorted[(top_n + 1):length(category_counts_sorted)])
            category_counts_top_n <- category_counts_sorted[1:top_n]
            category_counts_top_n['Others'] <- other_count
          } else {
            category_counts_top_n <- category_counts_sorted
          }
          
          # Calculate the percentage for each category.
          category_percentage <- prop.table(category_counts_top_n) * 100
          pie(category_percentage, 
              labels = paste(round(category_percentage, 2), "%"), 
              main = paste("Distribution of Top", top_n, input$x_axis),
              col = rainbow(length(category_percentage)))
          legend("topright", legend = names(category_counts_top_n), fill = rainbow(length(category_percentage)), title = "Top Categories")
        }
      }
    }
    
    # Density Plot
    if (input$plot_type == "Density Plot" && !is.null(input$x_axis)) {
      selected_data <- youtube[[input$x_axis]]
      if (is.numeric(selected_data) && !is.null(selected_data)) {
        selected_data <- na.omit(selected_data)
        ggplot(youtube, aes_string(x = input$x_axis)) +
          geom_density(fill = "skyblue", alpha = 0.5) +
          labs(title = paste("Density Plot of", input$x_axis),
               x = input$x_axis, 
               y = "Density") +
          theme_minimal() +
          theme(
            plot.title = element_text(face = "bold", hjust = 0.5, size = 16),
            axis.title = element_text(size = 14),
            axis.text = element_text(size = 12)
          )
      }
    }
  })
}

# Run the shiny application 
shinyApp(ui = ui, server = server)
