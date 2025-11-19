# Username og Password er taget ud af connectionstring, da der gøres brug af Trusted_Connection=True i stedet som benytter brugeren der i forvejen er logget ind, som i dette tilfælde er funpark\Administrator
# Database connection
$Server = "SQL01\SQL01"
$Database = "Funpark"
#$Username = "funpark\Administrator"
#$Password = "Lucasersej123"
$ConnectionString = "Server=$Server;Database=$Database;Trusted_Connection=True;"
#User ID=$Username;Password=$Password;



# Funktion til at lukke menuen i do loop - Returnere en write-host der får menuen til at lukke.
function CloseMenu {
    $Close = Write-Host -ForegroundColor Cyan "`nLukker for indberetning"
    return $Close
}



# Funktion til at åbne en forbindelse imod SQL databasen med brug af ovenstående connectionstring
function SqlConnection {
    $Connection = New-Object System.Data.SqlClient.SqlConnection
    $Connection.ConnectionString = $ConnectionString
    $Connection.Open()
    return $Connection
}



# Funktion til at indberette kø tider på specifikke forlystelser
# Medarbejderen får vist en liste over forlystelser, og skal efterfølgende indtaste sit medarbejdernummer
# Efterfølgende skal medarbejderen indtaste hvilken forlystelse det drejer sig om samt køtiden i minutter
# Indberetningen bliver indsat i databasen via querien som indeholder de indtastede værdier
# Funktionen er bygget op med en try, catch og finally -> Kører først det i try og hvis der er en fejl bliver den fanget i catchen, hvor den til sidst kører finally.
function QueueTimeReport {
    # Gemmer SQL forbindelsen i en variabel til videre behandling
    $Connection = SqlConnection
    try {
        # Medarbejderen får i første omgang vist alle oprettede forlystelser via en SELECT statement på tabellen ride
        # Samler SQL querien i en variabel sammen med db connection string
        $Sql = $Connection.CreateCommand()
        $Sql.CommandText = "SELECT ride_id, ride_name FROM ride ORDER BY ride_name"

        # Der gøres brug af SqlDataAdapter til at udføre SQL querien som er gemt i $Sql
        # Her gemmes SQL resultaterne i en variabel $SqlData
        # Til sidst bliver resultaterne fyldt ind i variablen $SqlData
        $SqlAdapt = New-Object System.Data.SqlClient.SqlDataAdapter $Sql
        $SqlData = New-Object System.Data.Datatable
        $SqlAdapt.Fill($SqlData) | Out-Null

        # if/else statement til at vise alle forlystelser
        # Hvis der ingen rækker er -> Udskriv ingen forlystelser
        # Ellers bliver der lavet et for loop til at vise alle rækker fra SQL querien gemt i $SqlData
        if ($SqlData.Rows.Count -eq 0) {
            Write-Host "Der blev ikke fundet nogle forlystelser" -ForegroundColor Red
        } else {
            Write-Host "`nTilgængelige forlystelser:`n" -ForegroundColor Cyan
            for ($i = 0; $i -lt $SqlData.Rows.Count; $i++) {
                Write-Host "$($i + 1). $($SqlData.Rows[$i]["ride_name"])"
            }
        }

        # I et do loop promptes medarbejderen til indtastning af medarbejder nummer
        # Her skal indtastningen være en int (tal) og over 0, ellers fortsætter loopet
        do {
            $InputEmployee = Read-Host "`nIndtast dit medarbejder nummer"
        } while (-not ($InputEmployee -as [int]) -or $InputEmployee -lt 1 -or $InputEmployee -gt $SqlData.Rows.Count)

        # Her spørger man brugeren om hvilken forlystelse det drejer sig om
        # Her skal indtastningen være en int (tal) og over 0, ellers fortsætter loopet
        do {
            $InputRide = Read-Host "`nIndtast nummeret på forlystelsen du ønsker at indberette for"
        } while (-not ($InputRide -as [int]) -or $InputRide -lt 1 -or $InputRide -gt $SqlData.Rows.Count)

        # Da powershell starter fra 0 af i et index, så trækkes der 1 fra det indtastede resultat så det passer og gemmer i en variabel
        $InputChoiceEmployee = $SqlData.Rows[$InputEmployee - 1]
        $InputChoiceRide = $SqlData.Rows[$InputRide - 1]
        $Ride_ID = $InputChoiceRide["ride_id"]
        $Ride_Name = $InputChoiceRide["ride_name"]


        # Her spørger ham brugeren om hvor lang kø tiden er på den bestemte forlystelse
        # Her skal indtastningen være en int (tal) og over 0, ellers fortsætter loopet
        do {
            $QueueReportTime = Read-Host "`nIndtast kø tiden i minutter for '$Ride_Name'"
        } while (-not ($QueueReportTime -as [int]) -or $QueueReportTime -lt 0)


        # Her indsendes rapporteringen til databasen
        # Igen pakkes SQL forbindelsen sammen med oprettelse af SQL querien.
        $SqlInsert = $Connection.CreateCommand()
        $SqlInsert.CommandText = @"
            # Her laves INSERT querien klar med værdierne, som medarbejderen kommer til at taste ind.
            INSERT INTO queue_report (time_in_minutes, ride_id, employee_id)
            VALUES (@time_in_minutes, @ride_id, @employee_id)
"@
        # Den gemte query i SqlInsert får nu de indtastede værdier som parametre
        $SqlInsert.Parameters.AddWithValue("@ride_id", $Ride_ID) | Out-Null
        $SqlInsert.Parameters.AddWithValue("@time_in_minutes", $QueueReportTime) | Out-Null
        $SqlInsert.Parameters.AddWithValue("@employee_id", $InputEmployee) | Out-Null

        # Nu eksekveres querien med det indtastede parametre som værdier, og viser de indtastede værdier efterfølgende i en write-host.
        $SqlInsert.ExecuteNonQuery() | Out-Null
        Write-Host "`nIndberetningen af kø tid for '$Ride_Name' var succesfuld. Der blev indberettet '$QueueReportTime' minutter" -ForegroundColor Green
        sleep 4
        # Sat en Read-Host ind for at medarbejderen kan tage stilling til resutatet. Hvis denne ikke er her lukker menuen med det samme.
        Read-Host "`nTryk 'Enter' for at lukke menuen"
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    # Til sidst lukker man forbindelsen til SQL serveren
    finally {
        $connection.Close()
    }

}



# Funktion til at vise seneste indberetninger på forlystelser.
# Medarbejderen får vist alle seneste indberetninger på forlystelser, hvor den højeste dato kun vises på hver forlystelse.
# Funktionen er bygget op med en try, catch og finally -> Kører først det i try og hvis der er en fejl bliver den fanget i catchen, hvor den til sidst kører finally.
function ShowRides {
    # Gemmer SQL forbindelsen i en variabel til videre behandling
    $Connection = SqlConnection
    try {
        # Samler SQL querien i en variabel sammen med db connection string
        $Sql = $Connection.CreateCommand()
        $Sql.CommandText = @"
            SELECT 
            r.ride_name,
            p.park_name,
            e.first_name + ' ' + e.last_name AS 'Indberettet',
            q.time_in_minutes,
            q.reported
            FROM queue_report q
            JOIN ride r ON q.ride_id = r.ride_id
            JOIN employees e ON q.employee_id = e.employee_id
            JOIN park p ON r.park_id = p.park_id
            WHERE q.reported = (
            -- SELECT MAX vælger den højeste værdi i en kolonne, dvs. der bliver valgt den højeste dato som også er den seneste.
                SELECT MAX(q2.reported)
                FROM queue_report q2
                WHERE q2.ride_id = q.ride_id
            )
            ORDER BY r.ride_name;
"@
    # Der gøres brug af SqlDataAdapter til at udføre SQL querien som er gemt i $Sql
    # Her gemmes SQL resultaterne i en variabel $SqlData
    # til sidst bliver resultaterne fyldt ind i en variabel
    $SqlAdapt = New-Object System.Data.SqlClient.SqlDataAdapter $Sql
    $SqlData = New-Object System.Data.Datatable
    $SqlAdapt.Fill($SqlData) | Out-Null

    Write-Host "`nOversigt over seneste køtid for hver forlystelse`n" -ForegroundColor Green
    # Resultaterne er blevet gemt i variablen $SqlData og her gøres der brug af et foreach loop til at vise alle rækkerne fra database tabellen.
    # Derudover er der lavet formateringen på rækkerne, hvor det første tal 0 er positionen for første række samt tallet ved siden af er padding, hvor minus er til højre for resultatet.
    foreach ($row in $SqlData.Rows) {
        Write-Host ("{0,-20} {1,-15} {2,-20} {3} min         {4}" -f `
        $row.ride_name, `
        $row.park_name, `
        $row.Indberettet, `
        $row.time_in_minutes, `
        $row.reported)
        }
        sleep 4
        # Sat en Read-Host ind for at medarbejderen kan tage stilling til resutatet. Hvis denne ikke er her lukker menuen med det samme.
        Read-Host "`nTryk 'Enter' for at lukke menuen"
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    # Til sidst lukker man forbindelsen til SQL serveren
    finally {
        $connection.Close()
    }
}



# Menu indeholder en do until statement med en switch. Når der trykkes 1 kalder den f.eks. QueueTimeReport og kører den funktion
do
{
    Clear-Host
    Write-Host "
        #----------------------------------------------------------#
        #                 Fun Park kø indberetning                 #
        #                                                          #
        #                                                          #
        #   1. Indberet kø tid                                     #
        #   2. Se seneste indberetning for alle forlystelser       #
        #                                                          #
        #   0. Luk indberetningsmenuen                             #
        #                                                          #
        #                                                          #
        #----------------------------------------------------------#
        "

    # Variablen $Menu indeholder en write-host som smager på input fra brugeren
    $Menu = Read-Host "Indtast valgmulighed"

    # Switch som indeholder alle funktionerne og bliver kaldt når der trykkes fra 1 - 2. Switchen smager på $Menu
    # default med en write-host når der indstastes noget der ikke er i switchen
    switch ($Menu)
    {
        1 {QueueTimeReport}
        2 {ShowRides}
        0 {CloseMenu}
            
        # Hvis forkert valg starter man forfra til hovedmenu funktion
        default 
        {
            Write-Host -ForegroundColor red "Forkert valgmulighed"
            sleep 2
        }
    }
    # Until som smager på variablen $Menu som kigger på om variablen ikke er lige med true - Kører funktionen CloseMenu hvis false -> 0
} until ($Menu -ne $true)
