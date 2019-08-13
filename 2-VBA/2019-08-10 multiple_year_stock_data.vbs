Sub stock_data()

For Each ws In Worksheets

Dim ticker As String
Dim volume As Double
volume = 0
Dim op As Double
Dim cls As Double
Dim yr_chg As Double
Dim pct_chg As Double
Dim summary_table_row As Long
summary_table_row = 2

ws.Cells(1, 9) = "Ticker"
ws.Cells(1, 10) = "Yearly Change"
ws.Cells(1, 11) = "Percent Change"
ws.Cells(1, 12) = "Total Stock Volume"

op = ws.Cells(2, 3).Value
lastrow = ws.Cells(Rows.Count, 1).End(xlUp).Row
    
    For i = 2 To lastrow
    
        If ws.Cells(i + 1, 1).Value <> ws.Cells(i, 1).Value Then

            ticker = ws.Cells(i, 1).Value
            ws.Cells(summary_table_row, 9).Value = ticker
        
            cls = ws.Cells(i, 6).Value
            
            yr_chg = cls - op
            ws.Cells(summary_table_row, 10).Value = yr_chg
        
            If (op = 0 And cls = 0) Then
            pct_chg = 0
            ElseIf (op = 0 And cls <> 0) Then
            pct_chg = 1
            Else
            pct_chg = yr_chg / op
            ws.Cells(summary_table_row, 11).Value = pct_chg
            ws.Cells(summary_table_row, 11).NumberFormat = "0.00%"
            End If
        
            volume = volume + ws.Cells(i, 7).Value
            ws.Cells(summary_table_row, 12).Value = volume
            
            summary_table_row = summary_table_row + 1
            volume = 0
            op = ws.Cells(i + 1, 3).Value
        
        Else
        
        volume = volume + ws.Cells(i, 7).Value
        
        End If
        
    Next i
    
lastrow = ws.Cells(Rows.Count, 10).End(xlUp).Row
    
    For j = 2 To lastrow
    
        If ws.Cells(j, 10).Value > 0 Or ws.Cells(j, 10) = 0 Then
            ws.Cells(j, 10).Interior.ColorIndex = 10
            Else
            ws.Cells(j, 10).Interior.ColorIndex = 3
        End If
        
    Next j
    
ws.Cells(2, 15) = "Greatest % Increase"
ws.Cells(3, 15) = "Greatest % Decrease"
ws.Cells(4, 15) = "Greatest Total Volume"
ws.Cells(1, 16) = "Ticker"
ws.Cells(1, 17) = "value"

lastrow = ws.Cells(Rows.Count, 10).End(xlUp).Row

    For k = 2 To lastrow
    
        If ws.Cells(k, 11).Value = Application.WorksheetFunction.Max(ws.Range("K2:K" & lastrow)) Then
        ws.Cells(2, 16).Value = ws.Cells(k, 9).Value
        ws.Cells(2, 17).Value = ws.Cells(k, 11).Value
        ws.Cells(2, 17).NumberFormat = "0.00%"
        ElseIf ws.Cells(k, 11).Value = Application.WorksheetFunction.Min(ws.Range("K2:K" & lastrow)) Then
        ws.Cells(3, 16).Value = ws.Cells(k, 9).Value
        ws.Cells(3, 17).Value = ws.Cells(k, 11).Value
        ws.Cells(3, 17).NumberFormat = "0.00%"
         ElseIf ws.Cells(k, 12).Value = Application.WorksheetFunction.Max(ws.Range("L2:L" & lastrow)) Then
        ws.Cells(4, 16).Value = ws.Cells(k, 9).Value
        ws.Cells(4, 17).Value = ws.Cells(k, 12).Value
    
        
        End If
    
    Next k

Next ws
  
End Sub

