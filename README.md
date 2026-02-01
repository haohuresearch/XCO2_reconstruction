# XCO₂ Reconstruction

## File Overview

This repository contains the main scripts and notebooks used for global XCO₂ reconstruction, model training, prediction, and analysis.

### 1. `Feature_Engineering.ipynb`
**Input:**  
- Resampled feature variables  
- Target variables  

**Function:**  
- Perform feature engineering on input variables  
- Convert original NetCDF (`.nc`) files into NumPy (`.npy`) format for efficient Python-based processing  

**Output:**  
1. Processed XCO₂ spatiotemporal feature datasets  
2. Converted `.npy` files corresponding to the original `.nc` inputs  

---

### 2. `plot_corr_figure.ipynb`
**Function:**  
- Conduct correlation analysis on non-spatial datasets after feature engineering  

---

### 3. `XCO2_training.ipynb`
**Input:**  
- Non-spatial XCO₂ samples after feature engineering  
- Corresponding feature datasets  

**Function:**  
- Train an XGBoost-based regression model for XCO₂ reconstruction  

**Output:**  
- Trained model file: `xgb_xco2.json`  

---

### 4. `Prediction.ipynb`
**Input:**  
- Trained XGBoost model  
- Original input variables  

**Function:**  
1. Perform monthly batch prediction to avoid memory overflow  
2. Generate and save monthly global XCO₂ predictions  

**Output:**  
- Complete global XCO₂ daily datasets  
- Monthly `.npy` files covering the global domain  

---

### 5. `Compare_with_other_products.ipynb`
**Function:**  
- Compare the reconstructed XCO₂ product with TCCON observations and CAMS reanalysis data  

---

### 6. `plot_xco2_scatter_detail_map_figure.ipynb`
**Function:**  
- Plot global XCO₂ maps before and after reconstruction  
- Zoom into selected regions for detailed spatial comparison  

---

### 7. `plot_co2_seasonal_year.ipynb`
**Function:**  
- Analyze the seasonal cycle characteristics of global XCO₂  

---

### 8. `plot_co2_trend_time.ipynb`
**Function:**  
- Analyze long-term temporal trends in XCO₂  

---

### 9. `data_format_transfer.ipynb`
**Function:**  
- Convert reconstructed XCO₂ data from `.npy` format (generated in `Prediction.ipynb`) back to NetCDF (`.nc`) format for further analysis and data sharing  

---

## Notes
- This codebase is designed to support reproducible research for global XCO₂ reconstruction studies.
- Users are encouraged to cite the corresponding publication if this code is used in academic work.
