CREATE DATABASE lol_player_stats;

USE lol_player_stats;

CREATE TABLE Summoners (
	# Unique identifier for each player
    id INT PRIMARY KEY AUTO_INCREMENT,
    # Player's unique summoner ID
    summoner_id VARCHAR(255) NOT NULL,
    # Player's region 
    region VARCHAR(50) NOT NULL,
    # Player's account ID
    account_id VARCHAR(255) NOT NULL,
    # Player's persistent unique user ID
    puuid VARCHAR(255) NOT NULL,
    # In game player's name
    game_name VARCHAR(255) NOT NULL,
    # Player's tagline
    tagline VARCHAR(255),
    # Player's display name
    name_ VARCHAR(255) NOT NULL,
    # Internal name used by the platform
    internal_name VARCHAR(255) NOT NULL,
	# URL of the account profile picture
    profile_icon_url VARCHAR(255),
    # Player's account level
    level INT NOT NULL,
    # Last time player data was updated
    updated_at TIMESTAMP,
    # Time when player data is scheduled to be refreshed
    renewable_at TIMESTAMP
);

CREATE TABLE Summoners (
	# Unique identifier for each player
    id INT PRIMARY KEY AUTO_INCREMENT,
    # Player's unique summoner ID
    summoner_id VARCHAR(255) NOT NULL,
    # Player's region 
    region VARCHAR(50) NOT NULL,
    # Player's account ID
    account_id VARCHAR(255) NOT NULL,
    # Player's persistent unique user ID
    puuid VARCHAR(255) NOT NULL,
    # In game player's name
    game_name VARCHAR(255) NOT NULL,
    # Player's tagline
    tagline VARCHAR(255),
    # Player's display name
    name_ VARCHAR(255) NOT NULL,
    # Internal name used by the platform
    internal_name VARCHAR(255) NOT NULL,
	# URL of the account profile picture
    profile_icon_url VARCHAR(255),
    # Player's account level
    level INT NOT NULL,
    # Last time player data was updated
    updated_at TIMESTAMP,
    # Time when player data is scheduled to be refreshed
    renewable_at TIMESTAMP
);

CREATE TABLE Season_History (
	# Unique identifier for each season record
	id INT PRIMARY KEY AUTO_INCREMENT,
    # Links to the playe
    player_id INT NOT NULL,
    # The year of the season
    season INT NOT NULL,
    # Final rank of the player
    tier VARCHAR(255) NOT NULL,
    # Final division of the player
    division INT NOT NULL,
    # Final number of lps
    lp INT NOT NULL,
    # Link to the player
    FOREIGN KEY (player_id) REFERENCES Summoners(id) 
);

CREATE TABLE League_Stats (
	# Unique identifier for each stat records
    id INT PRIMARY KEY AUTO_INCREMENT,
    # Links to the player
    player_id INT,
    # Game mode
    queue_type VARCHAR(255),
    # Ranked tier in this queue
    tier VARCHAR(255),
    # Division within the tier
    division INT,
    # Number of lps
    lp INT,
    # Number of wins
    win INT,
    # Number of lose
    lose INT,
    # Winrate pourcentage
    winrate DECIMAL(4,2),
    
    FOREIGN KEY (player_id) REFERENCES Summoners(id)
);

CREATE TABLE Champion_Stats (
	# Unique identifier for each champion stats record
    id INT PRIMARY KEY AUTO_INCREMENT,
    # Links to the player
    player_id INT,
    # Name of the champion
    champion VARCHAR(255),
    # Number of wins with the champion
    win INT,
    # Number of lose with the champion
    lose INT,
    # Winrate in pourcentage with the champion
    winrate DECIMAL(4,2),
    # KDA ratio with the champion
    kda DECIMAL(4,2),
    
    FOREIGN KEY (player_id) REFERENCES Summoners(id)
);

CREATE TABLE Recent_Game_Stats (
	# Unique identifier for each recent game record
    id INT PRIMARY KEY AUTO_INCREMENT,
    # Links to the player
    player_id INT,
    # Name of the champion played in the game
    champion VARCHAR(255),
    # Number of kills
    kill_ INT,
    # Number of deaths
    death INT,
    # Number of assists
    assist INT,
    # Position played in the game
    position VARCHAR(255),
    # Is the game win or lost 
    is_win BOOLEAN,
    
    FOREIGN KEY (player_id) REFERENCES Summoners(id)
);


