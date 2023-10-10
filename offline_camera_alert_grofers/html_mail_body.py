def html_str(table_data):
    html_ = '''
      <html>
      <body>
      <p><em>Alert generation logic:</em></p>
<ul>
    <li>Any email ID added before 23:59:59 hrs, will start getting alerts from the next day.</li>
    <li>All cameras that are offline, their names will be included.</li>
    <li>To solve this, do the following:</li>
        <ul>
            <li>Start Darsa software</li>
            <li>Check if PC internet is working, by taking remote AnyDesk from any other PC or mobile phone</li>
            <li>Check if cameras are streaming in the VLC (of the PC where software is installed)</li>
            <li>If all of the above are fine, contact Darsa team</li>
        </ul>
    </li>
</ul>
      
<table style="border: 1px solid orange; border-collapse: collapse">
  <tr>
    <th style="border: 1px solid orange">Camera</th>
    <th style="border: 1px solid orange">Facility</th>
  </tr>

{0}
</table>
</body>
</html>
'''.format(table_data)
    return html_