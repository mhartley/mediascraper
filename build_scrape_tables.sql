select * from bb_fb_trump_articles limit 1000;


delete from bb_fb_trump_articles where id = 1;


##there was a bunch of bad characters that got thrown in unicode conversion. removing them. 

select headline, replace(replace(replace(replace(replace(replace(headline, 'â', ''), '™', ''), '€', ''), 'â', ''),'˜', ''), 'â€"', '') from bb_fb_trump_articles limit 100;

update bb_fb_trump_articles
set 
headline = replace(replace(replace(replace(replace(replace(headline, 'â', ''), '™', ''), '€', ''), 'â', ''),'˜', ''), 'â€"', ''),
par1 = replace(replace(replace(replace(replace(replace(par1, 'â', ''), '™', ''), '€', ''), 'â', ''),'˜', ''), 'â€"', '');


update bb_fb_trump_articles
set 
par1 = replace(replace(par1, 'Â', ''), 'œ', ''),
headline = replace(replace(headline, 'Â', ''), 'œ', '');

select substring(link, locate('2', link), 10) from bb_fb_trump_articles limit 20;

alter table bb_fb_trump_articles add column textdate varchar(255);

 update bb_fb_trump_articles set textdate =  substring(link, locate('20', link), 10);
 
 select * from bb_fb_trump_articles where textdate = ''; #246 not matching
 
#they basically go in chronologically, so we can fill in those null values with the previous date adnd get a 24 hour approximation. Good enough for me!  
create temporary table t (
select @id := id id, textdate, 
(case when textdate =''
	then (select textdate from bb_fb_trump_articles where id = @id-1) 
else textdate end) textdate2
 from bb_fb_trump_articles);
 
 drop table t;
 
 select * from t;
 
 update bb_fb_trump_articles a
 join t b on a.id = b.id
 set a.textdate = b.textdate2;
 
 #16 rows still blank, removing them.
 delete from bb_fb_trump_articles where textdate = '';
 
 #check to make sure all values are in valid format
 select * from bb_fb_trump_articles where textdate not rlike '[0-9]{4}/[0-9]{2}/[0-9]{2}';
 
 ###noo! There is a category called '2016-presidential race', and we get 851 failures. Let's define a function for n-th substring and fix it.
 
 DELIMITER //
CREATE FUNCTION LOCATE_OFFSET(substr text, str text, offset int)
RETURNS int
DETERMINISTIC
BEGIN
DECLARE loc INT DEFAULT 1;
DECLARE i INT DEFAULT 0;
WHILE(i<offset) DO
SET loc=LOCATE(substr, str, loc+1);
SET i=i+1;
END WHILE;
RETURN(loc);
END//
DELIMITER ;

create temporary table t (
 select * from bb_fb_trump_articles where textdate not rlike '[0-9]{4}/[0-9]{2}/[0-9]{2}');
 
update t set textdate =  substring(link, locate_offset('20', link, 2), 10);

#okay, now we've sovled that problem. There are still a bunch of fact checks that still don't register dates, but they are not that relevant and we are going to drop them.
#I can't believe I forgot to add dates to the scraper! What a pain... doing that next.

delete from t where textdate = ''; #56 rows dropped

#run this again...
 update bb_fb_trump_articles a
 join t b on a.id = b.id
 set a.textdate = b.textdate;

delete from bb_fb_trump_articles where textdate not rlike '[0-9]{4}/[0-9]{2}/[0-9]{2}';  ## a bunch of random stuff in here. 57 articles dropped

##okay, let's delete where the scraper messed up and we don't have headlines or body text
delete from bb_fb_trump_articles where headline is null; #23 rows dropped
delete from bb_fb_trump_articles where par1 is null; #9 rows dropped

select count(*) from bb_fb_trump_articles;  #12173 survivors! 
 
 
 #put the date in a respectable date format for mysql
 update bb_fb_trump_articles
 set pub_date = cast(replace(textdate, '/', '-') as date); #zero warnings! Yay for good data cleaning.
 
select * from bb_fb_trump_articles;
alter table bb_fb_trump_articles drop column textdate;
 
 

 
 
 
 
 select * from bb_fb_trump_articles;
 
 
 create table guardian_articles (
 id int primary key auto_increment,
link varchar(500),
headline varchar(1000),
pars text);
 
 
  create table huffpost_articles (
 id int primary key auto_increment,
link varchar(500),
headline varchar(1000),
pars text);

#load data files were actually run server side after scping the source. Here for recording sake.
 
load data local infile '/home/ubuntu/bbscrape/hpdata.csv' into table huffpost_articles fields terminated by '|' lines terminated by '\n'  (link, headline, pars);
load data local infile '/home/ubuntu/bbscrape/gudata.csv' into table guardian_articles fields terminated by '|' lines terminated by '|||'  (link, headline, pars);
 
 select * from huffpost_articles;
 select * from guardian_articles;
 
 
 
