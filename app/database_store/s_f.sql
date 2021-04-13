
CREATE TABLE  IF NOT EXISTS `sales_forecasting` (
	`ds` TIMESTAMP,
	`trend` FLOAT,
	`yhat_lower` FLOAT,
	`yhat_upper` FLOAT,
	`trend_lower` FLOAT,
	`trend_upper` FLOAT,
	`additive_terms` FLOAT,
	`additive_terms_lower` FLOAT,
	`additive_terms_upper` FLOAT,
	`weekly` FLOAT,
	`weekly_lower` FLOAT,
	`weekly_upper` FLOAT,
	`yearly` FLOAT,
	`yearly_lower` FLOAT,
	`yearly_upper` FLOAT,
	`multiplicative_terms` FLOAT,
	`multiplicative_terms_lower` FLOAT,
	`multiplicative_terms_upper` FLOAT,
	`yhat` FLOAT,
	PRIMARY KEY (`ds`)
);

CREATE TABLE `city` (
  `ds` TIMESTAMP,
  `cityName` varchar(30) NOT NULL
  PRIMARY KEY (`ds`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
