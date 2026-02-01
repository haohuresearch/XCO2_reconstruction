/////////////////////////////////////////////////////////////////////
//mcd12c1 land use
///////////////////////////////////////////////////////////////////////
//加载数据集并筛选2019-2023年
var dataset = ee.ImageCollection('MODIS/061/MCD12C1')
  .filterDate('2019-01-01', '2024-01-01')
  .select('Majority_Land_Cover_Type_1');

// 全球范围
var global =ee.Geometry.Rectangle([-180, -90, 180, 90], null, false);

// 逐年导出（利用年度产品特性，每年1张影像）
for (var year = 2019; year <= 2023; year++) {
  // 筛选单一年份影像
  var img = dataset
    .filterDate(year + '-01-01', (year + 1) + '-01-01')
    .first()
    .rename('LandCover_' + year);
  
  // 导出到Google Drive
  Export.image.toDrive({
    image: img,
    description: 'MCD12C1_landuse' + year, // 文件名含年份
    folder: 'GEE_LandCover', // Drive文件夹名
    region: global,
    crs: 'EPSG:4326',
    scale: 11000, // 分辨率（500m可选，文件较大）
    maxPixels: 1e13 // 允许全球范围导出
  });
}