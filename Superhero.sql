use superhero;
show tables;

select * from alignment;
select * from comic;
select * from superhero;
select * from colour; # 4 is black, 9 is brown, 10 is brown/black, 31 is white, 33 is yellow (asian?)
select * from attribute;
select * from publisher; # 4 for DC, 3 for Dark Horse and 13 for Marvel

select
	count(id) as total_n_sh
from superhero; #750

-- Let's count the data for publisher (Marvel and DC only)
SELECT
    count(id) as DC_sh
from superhero
where publisher_id = 4;

SELECT
    count(id) as Marvel_sh
from superhero
where publisher_id = 13;

SELECT
    count(id) as Total_publisher_sh
from superhero
where publisher_id = 13 OR publisher_id = 4;

-- Let's see how many black superheroes do we have
select
    count(case when skin_colour_id = 4 or skin_colour_id = 9 or skin_colour_id = 10 then id end) as black_sh -- 1, so it's definitely wrong
from superhero;

select 
    superhero_name,
    skin_colour_id
from superhero
where superhero_name = 'Black Panther'
group by superhero_name, skin_colour_id
order by superhero_name desc;

-- Black people are not really counted in this database, not for humans at least, even if there's a skin_coulour_id.

select 
    superhero_name,
    skin_colour_id,
    publisher_id
from superhero
where superhero_name = 'Alien';

select 
    superhero_name,
    skin_colour_id,
    publisher_id
from superhero
where superhero_name = 'Superman';

-- And how about women?
select
    count(case when gender_id = 1 then id end) as male_sh,
    count(case when gender_id = 2 then id end) as female_sh,
    count(case when gender_id = 3 then id end) as not_defined_sh,
    count(case when gender_id is NULL then id end) as not_known_sh
from superhero;

-- The most intelligent in DC and Marvel?
SELECT 
    s.superhero_name,
    ha.attribute_value,
    p.publisher_name
FROM superhero s
LEFT JOIN 
    hero_attribute ha ON s.id = ha.hero_id
LEFT JOIN 
    attribute a ON ha.attribute_id = a.id
LEFT JOIN
    publisher p ON s.publisher_id = p.id
WHERE ha.attribute_id = 1 AND ha.attribute_value = 100 
AND (s.publisher_id = 4 OR s.publisher_id = 13)
ORDER BY ha.attribute_value DESC;

-- The stronguest character?

SELECT 
    s.superhero_name,
    ha.attribute_value,
    p.publisher_name
FROM superhero s
LEFT JOIN 
    hero_attribute ha ON s.id = ha.hero_id
LEFT JOIN 
    attribute a ON ha.attribute_id = a.id
LEFT JOIN
    publisher p ON s.publisher_id = p.id
WHERE ha.attribute_id = 2 AND ha.attribute_value = 100 
AND (s.publisher_id = 4 OR s.publisher_id = 13)
ORDER BY ha.attribute_value DESC;

-- What are the individual attributes and combined strength of the Justice League members?
select 
    s.superhero_name,
    ha.attribute_value as strength,
    (
        select sum(ha2.attribute_value)
        from superhero s2
        left join hero_attribute ha2 on s2.id = ha2.hero_id and ha2.attribute_id = 2
        where s2.superhero_name in ('Batman', 'Superman', 'Wonder Woman', 'Aquaman', 'Flash', 'Green Lanter', 'Martian Manhunter')
    ) as total_group_strength
from superhero s
left join hero_attribute ha on s.id = ha.hero_id and ha.attribute_id = 2
where s.superhero_name in ('Batman', 'Superman', 'Wonder Woman', 'Aquaman', 'Flash', 'Green Lanter', 'Martian Manhunter')
group by s.superhero_name, ha.attribute_value
order by s.superhero_name desc;

-- And what about the Avengers? Who's stronger?
select 
    s.superhero_name,
    ha.attribute_value as strength,
    (
        select sum(ha2.attribute_value)
        from superhero s2
        left join hero_attribute ha2 on s2.id = ha2.hero_id and ha2.attribute_id = 2
        where s2.superhero_name in ('Hulk', 'Iron Man', 'Thor', 'Captain America', 'Haweye', 'Black Widow', 'Ant-Man')
    ) as total_group_strength,
    (
        select avg(ha2.attribute_value)
        from superhero s2
        left join hero_attribute ha2 on s2.id = ha2.hero_id and ha2.attribute_id = 2
        where s2.superhero_name in ('Hulk', 'Iron Man', 'Thor', 'Captain America', 'Haweye', 'Black Widow', 'Ant-Man')
    ) as avg_group_strength

from superhero s
left join hero_attribute ha on s.id = ha.hero_id and ha.attribute_id = 2
where s.superhero_name in ('Hulk', 'Iron Man', 'Thor', 'Captain America', 'Haweye', 'Black Widow', 'Ant-Man')
group by s.superhero_name, ha.attribute_value
order by s.superhero_name desc;

-- What is the most frequent superpower?
select 
    sp.power_name as superpower,
    count(hp.hero_id) as frequency
from superpower sp
inner JOIN hero_power hp ON sp.id = hp.power_id
inner join superhero sh ON hp.hero_id = sh.id
GROUP BY sp.power_name
ORDER BY frequency DESC
limit 1;

-- What is the hero with the biggest number of superpowers?
select
    sh.superhero_name,
    count(hp.power_id) as total_powers,
    al.alignment as Good_or_Evil
from superhero sh
left join alignment al
    on sh.alignment_id = al.id
inner join hero_power hp
    on hp.hero_id = sh.id
inner join superpower sp
    on sp.id = hp.power_id
group by sh.superhero_name, al.alignment
order by total_powers desc
limit 1;

-- What is the smallest and the biggest superhero?

select 
    superhero_name,
    height_cm as biggest_superhero
from superhero
where publisher_id = 4 OR publisher_id = 13
order by biggest_superhero desc;

select 
    superhero_name,
    height_cm as smallest_superhero
from superhero
where (publisher_id = 4 OR publisher_id = 13) AND height_cm > 0
order by smallest_superhero asc;