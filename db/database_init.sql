CREATE TABLE `Participant` (
	`id` int NOT NULL AUTO_INCREMENT,
	`score` DECIMAL NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Team` (
	`id` int NOT NULL AUTO_INCREMENT,
	`name` varchar(63) NOT NULL UNIQUE,
	`participant id` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `User` (
	`id` int NOT NULL AUTO_INCREMENT,
	`username` varchar(63) NOT NULL,
	`email` varchar(127) NOT NULL UNIQUE,
	`password hash` varchar(255) NOT NULL,
	`password salt` varchar(63) NOT NULL UNIQUE,
	`participant id` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Challenge` (
	`id` int NOT NULL AUTO_INCREMENT,
	`category id` int NOT NULL,
	`text` varchar(511) NOT NULL,
	`team id` int NOT NULL,
	`solution id` int NOT NULL,
	`points` int NOT NULL,
	`docker image` varchar(255) NOT NULL UNIQUE,
	`status` bool NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Solution` (
	`id` int NOT NULL AUTO_INCREMENT,
	`path` varchar(511) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Competition` (
	`id` int NOT NULL AUTO_INCREMENT,
	`team id` int NOT NULL,
	`challenge id` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Category` (
	`id` int NOT NULL AUTO_INCREMENT,
	`category` varchar(15) NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `Team` ADD CONSTRAINT `Team_fk0` FOREIGN KEY (`participant id`) REFERENCES `Participant`(`id`);

ALTER TABLE `User` ADD CONSTRAINT `User_fk0` FOREIGN KEY (`participant id`) REFERENCES `Participant`(`id`);

ALTER TABLE `Challenge` ADD CONSTRAINT `Challenge_fk0` FOREIGN KEY (`category id`) REFERENCES `Category`(`id`);

ALTER TABLE `Challenge` ADD CONSTRAINT `Challenge_fk1` FOREIGN KEY (`team id`) REFERENCES `Team`(`id`);

ALTER TABLE `Challenge` ADD CONSTRAINT `Challenge_fk2` FOREIGN KEY (`solution id`) REFERENCES `Solution`(`id`);

ALTER TABLE `Competition` ADD CONSTRAINT `Competition_fk0` FOREIGN KEY (`team id`) REFERENCES `Team`(`id`);

ALTER TABLE `Competition` ADD CONSTRAINT `Competition_fk1` FOREIGN KEY (`challenge id`) REFERENCES `Challenge`(`id`);
