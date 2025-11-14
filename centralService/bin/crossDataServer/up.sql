CREATE TABLE IF NOT EXISTS guild_relation (
    guild_pair VARCHAR(255) NOT NULL,
    relation_type INT NOT NULL,
    end_time INT NOT NULL,
    PRIMARY KEY (guild_pair)
);

CREATE TABLE IF NOT EXISTS relation_version (
    id INT NOT NULL AUTO_INCREMENT,
    version INT NOT NULL,
    PRIMARY KEY (id)
)
