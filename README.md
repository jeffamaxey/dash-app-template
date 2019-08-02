There are three main layout components in dash-bootstrap-components: Container, Row, and Col.

- The Container component can be used to center and horizontally pad your app's content. By default the container has a responsive pixel width. Use the keyword argument `fluid=True` if you want your Container to fill available horizontal space and resize fluidly.
- The Row component is a wrapper for columns. The layout of your app should be built as a series of rows of columns.
- When using the grid layout, content should be placed in columns, and only Col components should be immediate children of Row.
- By default, columns will have equal **width** and will expand to fill available space.
    - Specify the desired width of each column using the `width` keyword argument.
    - `width=True` will cause the Col to expand and fill available space
    - `width=auto` will adapt to the content in the Col
    - `width=1,2,...12` will cause the Col to span *n* of the 12-Cols of the grid. For example, a Col with `width=6` will fill half the space of the parent.
- Control the **vertical alignment** of each column in the row using the `align` keyword
    - available options are "start", "center", "end"
- Control **horizontal alignment** of columns using the `justify` keyword argument of Row. The options are "start", "center", "end", "between" and "around".    
