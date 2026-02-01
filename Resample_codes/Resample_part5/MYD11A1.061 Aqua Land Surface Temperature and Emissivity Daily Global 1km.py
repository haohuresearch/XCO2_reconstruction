//////////////////////////////////////////////////////////////////////////
//MYD11A1.061 Aqua Land Surface Temperature and Emissivity Daily Global 1km
//////////////////////////////////////////////////////////////////////////
设置年份
var year = 2022;

// 定义全球范围
var globalRegion = ee.Geometry.Rectangle([-180, -90, 180, 90], null, false);

// 循环每个月
for (var month = 1; month <= 12; month++) {
  
  // 构造开始和结束日期
  var start = ee.Date.fromYMD(year, month, 1);
  var end = start.advance(1, 'month');

  // 读取 ERA5 数据
  var era5_2mt = ee.ImageCollection('MODIS/061/MYD11A1')
    .filterDate(start, end)
    .select('LST_Day_1km');

  // 如果该月没有数据，跳过
  var count = era5_2mt.size();
  print('Month:', month, 'Image count:', count);
  if (count.getInfo() === 0) {
    continue;
  }

  // 转为多波段影像（波段名为日期）
  var era5_bands = era5_2mt.toBands();
  var bandNames = era5_2mt.aggregate_array("system:time_start")
    .map(function(time) {
      return ee.Date(time).format('YYYYMMdd');
    });
  era5_bands = era5_bands.rename(bandNames);

  // 定义导出任务
  Export.image.toDrive({
    image: era5_bands.clip(globalRegion),
    description: 'MYD11A1_' + year + '_' + (month < 10 ? '0' + month : month),
    folder: '2022Land_Surface_Temperature_and_Emissivity',
    fileNamePrefix: 'MYD11A1_' + year + '_' + (month < 10 ? '0' + month : month) + '_Global',
    region: globalRegion,
    scale: 11000,
    crs: 'EPSG:4326',
    maxPixels: 1e13
  });
}