<p align="center"><img src='https://user-images.githubusercontent.com/50906588/206149285-a241e24f-437a-4825-9276-b573eec606dc.png' height=180px/></p>

## How to run the frontend
There are several ways to run VariantHunter

### Using Docker (suggested)
Run the docker with the following commands:
- `docker pull gecopolimi/varianthunter`
- `{parameters_list} docker-compose up`

More details at http://cerilab.deib.polimi.it/variant_hunter/about#docker


### Deveploment only 
Run the docker with the following commands form /frontend folder:
- `npm install`
- `npm run serve`

To compile files for the backend run:
- `npm run build`