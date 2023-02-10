create table transformed_zillow_rental_listings as (
	select
		"zpid",
		"detailUrl" as url,
		"statusText" as housing_type,
		"unformattedPrice" as price,
		"address" as address,
		"addressStreet" as address_street,
		"addressCity" as city_street,
		"addressState" as state,
		"addressZipcode" as zipcode,
		case when "isUndisclosedAddress" then 1 else 0 end as undisclosed_address,
		"beds",
		"baths",
		"area" as sqft,
		"latitude",
		"longitude",
		cast("availabilityDate" as date) as date_available,
		"date_scraped" as date_scraped
	
	from zillow_rental_listings zrl 
)
;


