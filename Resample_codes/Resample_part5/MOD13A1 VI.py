//////////////////////////////////////////////////////////
//MOD13A1 VI
///////////////////////////////////////////////////////////
//定义研究区域（可以根据需要修改为特定区域）
var region = ee.Geometry.Rectangle([-180, -90, 180, 90], null, false);

// 定义数据集
var dataset = ee.ImageCollection('MODIS/061/MOD13A1');

// 定义年份范围
var startYear = 2019;
var endYear = 2025;

// 循环处理每一年
for (var year = startYear; year <= endYear; year++) {
  // 确定每年的开始和结束日期
  var startDate, endDate;
  
  if (year === endYear) {
    // 最后一年只到6月26日
    startDate = year + '-01-01';
    endDate = year + '-06-26';
  } else {
    // 其他年份全年
    startDate = year + '-01-01';
    endDate = year + '-12-31';
  }
  
  // 筛选该年份的数据并按时间排序
  var yearlyData = dataset
    .filter(ee.Filter.date(startDate, endDate))
    .sort('system:time_start');
  
  // 获取该年份影像的数量
  var count = yearlyData.size().getInfo();
  print('Year ' + year + ' image count: ', count);
  
  // 转换为列表以便处理
  var imageList = yearlyData.toList(count);
  
  // 存储处理后的NDVI和EVI影像列表
  var ndviImages = [];
  var eviImages = [];
  var dates = [];
  
  // 循环处理每一幅影像，提取NDVI和EVI并添加日期标识
  for (var i = 0; i < count; i++) {
    var image = ee.Image(imageList.get(i));
    var date = ee.Date(image.get('system:time_start')).format('yyyyMMdd').getInfo();
    dates.push(date);
    
    // 提取NDVI并应用比例因子，重命名波段为日期
    var ndvi = image.select('NDVI').multiply(0.0001).rename('NDVI_' + date);
    ndviImages.push(ndvi);
    
    // 提取EVI并应用比例因子，重命名波段为日期
    var evi = image.select('EVI').multiply(0.0001).rename('EVI_' + date);
    eviImages.push(evi);
  }
  
  // 合并一年中所有NDVI影像为一个多层影像（每年一个文件）
  var yearlyNDVI = ee.ImageCollection(ndviImages).toBands();
  
  // 合并一年中所有EVI影像为一个多层影像（每年一个文件）
  var yearlyEVI = ee.ImageCollection(eviImages).toBands();
  
  // 导出年度NDVI（一个文件包含全年所有时间点）
  Export.image.toDrive({
    image: yearlyNDVI,
    description: 'MODIS_NDVI_' + year,
    folder: 'MODIS_NDVI_EVI',
    scale: 11000,
    region: region,
    maxPixels: 1e13,
    fileFormat: 'GeoTIFF'
  });
  
  // 导出年度EVI（一个文件包含全年所有时间点）
  Export.image.toDrive({
    image: yearlyEVI,
    description: 'MODIS_EVI_' + year,
    folder: 'MODIS_NDVI_EVI',
    scale: 11000,
    region: region,
    maxPixels: 1e13,
    fileFormat: 'GeoTIFF'
  });
}