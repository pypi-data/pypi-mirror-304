from updater.utils.db_handler import db_get_specs_filters_by_brand_id
import asyncio

async def check_for_specs(product_brand: dict, product: dict) -> dict:

  ## Check if associated product has required specs in db
  brand_id = product_brand['brand_id']

  # Get specs_filters from pd_category
  specs_filters = await db_get_specs_filters_by_brand_id(brand_id)
  if specs_filters:
    # Check if product has specs in specs_filters
    for spec_filter in specs_filters:
      if spec_filter['label'] in product['specs']:
        print(f'-> Spec {spec_filter["label"]} found in product specs, no need to get')
      else:
        print(f'-> Spec {spec_filter["label"]} not found in product specs, getting specs...')
        asyncio.create_task(get_n_update_spec(spec_filter, product))
  else:
    return None
    
async def get_n_update_spec(spec_filter: dict, product: dict):
  if spec_filter['type'] == 'range':
    spec = await get_range_spec(spec_filter, product)
  elif spec_filter['type'] == 'options':
    spec = await get_options_spec(spec_filter, product)
  
  if spec:
    # Add spec to spec from product
    product['specs'][spec_filter['label']] = spec
    # Update spec in products table in db
    await db_update_product_spec(product['id'], product['specs'])
    

async def get_range_spec(spec_filter: dict, product: dict):
  print(f'-> Getting range spec {spec_filter["label"]}...')
  
  # Try to extract spec from product tilte and features
  
  
  return spec
  
  

async def get_options_spec(spec_filter: dict, product: dict):
  print(f'-> Getting options spec {spec_filter["label"]}...')




if __name__ == "__main__":
  product_brand = {
    'id': 1647,
    'brand_id': 1583,
    'product_id': 3168
  }
  product = {
    'id': 3168,
    'specs': {}
  }
  asyncio.run(check_for_specs(product_brand, product))