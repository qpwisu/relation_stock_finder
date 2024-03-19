use STOCK;

DROP TABLE IF EXISTS KR_STOCK_INFO_TB;
CREATE TABLE `KR_STOCK_INFO_TB` (
	`ticker`	VARCHAR(10)	NOT NULL,
	`company_name`	VARCHAR(20)	NULL,
	`market`	VARCHAR(10)	NULL,
	`company_description`	TEXT	NULL,
	`sector` VARCHAR(50) NULL,
    `market_cap` DECIMAL(20, 2) NULL,
    `per` FLOAT NULL,
    `eps` FLOAT NULL,
    `pbr` FLOAT NULL,
    `bps` FLOAT NULL,
    `divided` FLOAT NULL,
    `divided_rate` FLOAT NULL
);



ALTER TABLE `KR_STOCK_INFO_TB` ADD CONSTRAINT `PK_KR_STOCK_INFO_TB` PRIMARY KEY (
	`ticker`
);




drop table if exists KR_STOCK_PRICE_TB;
CREATE TABLE `KR_STOCK_PRICE_TB` (
	`date` DATE NOT NULL,
	`ticker` VARCHAR(10) NOT NULL,
	`open` DECIMAL(20,4) NULL,
	`high` DECIMAL(20,4) NULL,
	`low` DECIMAL(20,4) NULL,
	`close` DECIMAL(20,4) NULL,
	`volume` BIGINT NULL,
	`change_rate` DECIMAL(10,2) NULL,
	CONSTRAINT `FK_KR_STOCK_PRICE_TB_TICKER` FOREIGN KEY (`ticker`) REFERENCES `KR_STOCK_INFO_TB`(`ticker`)
);

ALTER TABLE `KR_STOCK_PRICE_TB` ADD CONSTRAINT `PK_KR_STOCK_PRICE_TB` PRIMARY KEY (`date`, `ticker`);



drop table if exists KR_STOCK_NEWS_TB;
CREATE TABLE KR_STOCK_NEWS_TB (
    newsID INT AUTO_INCREMENT,
    ticker VARCHAR(10),
    newsTitle TEXT,
    Date DATE,
    PRIMARY KEY (NewsID),
	CONSTRAINT `FK_KR_STOCK_NEWS_TB` FOREIGN KEY (`ticker`) REFERENCES `KR_STOCK_INFO_TB`(`ticker`)
);


drop table if exists KR_STOCK_THEMA_TB;
CREATE TABLE `KR_STOCK_THEMA_TB` (
	thema VARCHAR(30)	NOT NULL,
	PRIMARY KEY (thema)
);

drop table if exists thema_blog_TB;
CREATE TABLE `thema_blog_TB` (
	blog_id INT AUTO_INCREMENT,
	`thema`	VARCHAR(30)	NOT NULL,
	`title` text,
	`header`text,
	`href`text,
    Date DATE,
	PRIMARY KEY (blog_id),
	CONSTRAINT `FK_thema_TB` FOREIGN KEY (`thema`) REFERENCES `KR_STOCK_THEMA_TB`(`thema`)
);

drop table if exists blog_thema_analysis_TB;
CREATE TABLE `blog_thema_analysis_TB` (
	id INT AUTO_INCREMENT,
    blog_id INT,
	company_name VARCHAR(30)	NULL,
	PRIMARY KEY (id),
	CONSTRAINT `FK_thema_blog_TB` FOREIGN KEY (`blog_id`) REFERENCES `thema_blog_TB`(`blog_id`)
);

drop table if exists KR_STOCK_SECTOR_TB;
CREATE TABLE `KR_STOCK_SECTOR_TB` (
	sector VARCHAR(30)	NOT NULL,
	PRIMARY KEY (sector)
);

drop table if exists sector_blog_TB;
CREATE TABLE `sector_blog_TB` (
	blog_id INT AUTO_INCREMENT,
	`sector`	VARCHAR(30)	NOT NULL,
	`title` text,
	`header`text,
	`href`text,
    Date DATE,
	PRIMARY KEY (blog_id),
	CONSTRAINT `FK_sector_TB` FOREIGN KEY (`sector`) REFERENCES `KR_STOCK_SECTOR_TB`(`sector`)
);

drop table if exists blog_sector_analysis_TB;
CREATE TABLE `blog_sector_analysis_TB` (
	id INT AUTO_INCREMENT,
    blog_id INT,
	company_name VARCHAR(30)	NULL,
	PRIMARY KEY (id),
	CONSTRAINT `FK_sector_blog_TB` FOREIGN KEY (`blog_id`) REFERENCES `sector_blog_TB`(`blog_id`)
);




drop table if exists Politician_TB;
CREATE TABLE `Politician_TB` (
	`name`	VARCHAR(10)	NOT NULL,
	`party`	VARCHAR(10)	NULL,
	PRIMARY KEY (name)
);




drop table if exists politician_blog_TB;
CREATE TABLE `politician_blog_TB` (
	blog_id INT AUTO_INCREMENT,
	`name`	VARCHAR(10)	NOT NULL,
	`title` text,
	`header`text,
	`href`text,
    Date DATE,
	PRIMARY KEY (blog_id),
	CONSTRAINT `FK_Politician_TB` FOREIGN KEY (`name`) REFERENCES `Politician_TB`(`name`)
);

drop table if exists blog_stock_analysis_TB;
CREATE TABLE `blog_stock_analysis_TB` (
	id INT AUTO_INCREMENT,
    blog_id INT,
	`company_name` VARCHAR(20)	NULL,
	PRIMARY KEY (id),
	CONSTRAINT `FK_politician_blog_TB` FOREIGN KEY (`blog_id`) REFERENCES `politician_blog_TB`(`blog_id`)
);



drop table if exists total_stock_aggregate_TB;
CREATE TABLE total_stock_aggregate_TB (
	category VARCHAR(10)	NOT NULL,
	company_name	VARCHAR(10)	NOT NULL,
	cnt int not null,
    ranking int not null,
    period int not null,
	PRIMARY KEY (category,ranking,period)
);

drop table if exists total_category_aggregate_TB;
CREATE TABLE total_category_aggregate_TB (
	category VARCHAR(10)	NOT NULL,
	name VARCHAR(30)	NOT NULL,
	cnt int not null,
    ranking int not null,
    period int not null,
	PRIMARY KEY (category,ranking,period)
);

drop table if exists KR_NOW_STOCK_PRICE_TB;
CREATE TABLE `KR_NOW_STOCK_PRICE_TB` (
	`date` DATE NOT NULL,
	`ticker` VARCHAR(10) NOT NULL,
	`open` DECIMAL(20,4) NULL,
	`high` DECIMAL(20,4) NULL,
	`low` DECIMAL(20,4) NULL,
	`close` DECIMAL(20,4) NULL,
	`volume` BIGINT NULL,
	`change_rate` DECIMAL(10,2) NULL,
	`company_name`	VARCHAR(10)	NOT NULL,
	PRIMARY KEY (ticker),
	CONSTRAINT `FK_KR_NOW_STOCK_PRICE_TB` FOREIGN KEY (`ticker`) REFERENCES `KR_STOCK_INFO_TB`(`ticker`)

);

