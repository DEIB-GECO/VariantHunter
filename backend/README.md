<p align="center"><img src='https://i.postimg.cc/fLjL5q7K/Schermata-2022-06-12-alle-21-52-50.png' height=180px/></p>

## How to run the backend
There are several ways to run VariantHunter

### Using Docker (suggested)
Run the docker with the following commands:
- `docker pull gecopolimi/varianthunter`
- `{parameters_list} docker-compose up`

More details at http://cerilab.deib.polimi.it/variant_hunter/about#docker


### Locally 
Run the docker with the following commands form /backend folder:
- `pip3 install -r requirements.txt`
- `python3 ./app.py {parameter_list}`

For more details run `python3 ./app.py --help`