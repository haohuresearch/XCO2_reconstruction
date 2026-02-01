///////////////////////////////////////////////////////////////////////////
//VNP46A2 POPULATION
///////////////////////////////////////////////////////////////////////

// 加载VIIRS夜间灯光数据集
var dataset = ee.ImageCollection('NASA/VIIRS/002/VNP46A2');

// 设置参数
var year = 2025;
var scale = 11000; // 分辨率11000米
var region = ee.Geometry.Rectangle([-180, -90, 180, 90], null, false); // 全球范围
var bandName = 'Gap_Filled_DNB_BRDF_Corrected_NTL';

// 生成2019年每个月的日期范围
var months = ee.List.sequence(1, 12);
var monthsList = months.getInfo();

// 自定义月份补零函数（替代padStart）
function padMonth(month) {
  return month < 10 ? '0' + month : month.toString();
}

// 循环处理每个月
for (var i = 0; i < monthsList.length; i++) {
  var month = monthsList[i];
  
  // 计算每个月的开始和结束日期
  var startDate = ee.Date.fromYMD(year, month, 1);
  var endDate = startDate.advance(1, 'month');
  
  // 筛选当月数据
  var monthlyImage = dataset
    .filter(ee.Filter.date(startDate, endDate))
    .select(bandName)
    .mean()
    .rename(bandName);
  
  // 生成带补零的月份字符串（如1→"01"）
  var monthStr = padMonth(month);
  
  // 导出当月数据
  Export.image.toDrive({
    image: monthlyImage,
    description: 'VIIRS_NTL_' + year + '_' + monthStr, // 文件名格式: VIIRS_NTL_2019_01
    folder: 'VIIRS_DNB_VNP46A2_2025',
    region: region,
    scale: scale,
    crs: 'EPSG:4326',
    maxPixels: 1e13,
    fileFormat: 'GeoTIFF'
  });
}