# Happiness Dataset Analysis

## Introduction

The dataset we are analyzing revolves around various factors that impact happiness across different countries over the years. With a total of **2363 entries**, this dataset contains information on **165 unique countries** from **2005 to 2023**. The analysis of this dataset is crucial as it provides insights into the diverse aspects that affect the perception of happiness in different societies.

## Numerical Columns Overview

The numerical data is comprised of the following columns:

- **year**: The year in which the data was collected, ranging from 2005 to 2023.
- **Life Ladder**: A measure of subjective well-being on a scale from 0 to 10.
- **Log_GDP_per_capita**: The logarithm of GDP per capita, indicating the economic status of a country.
- **Social support**: Reflects the perceived support one receives from friends or family.
- **Healthy life expectancy at birth**: The average number of years a newborn is expected to live in good health.
- **Freedom to make life choices**: A measure of individual freedom in choosing one's path.
- **Generosity**: Represents the degree of charitable giving.
- **Perceptions of corruption**: A measure of people’s views on corruption in their country.
- **Positive affect**: The experience of positive emotions.
- **Negative affect**: The experience of negative emotions.

Here's a snapshot of the summary statistics for the numerical columns:

| Column                                         | Count   | Mean        | Std Dev    | Min   | 25%   | 50%   | 75%   | Max   |
|------------------------------------------------|---------|-------------|------------|-------|-------|-------|-------|-------|
| year                                           | 2363    | 2014.76     | 5.06       | 2005  | 2011  | 2015  | 2019  | 2023  |
| Life Ladder                                    | 2363    | 5.41        | 1.16       | 2.92  | 4.73  | 5.40  | 6.12  | 7.95  |
| Log_GDP_per_capita                            | 2330    | 9.82        | 1.29       | 7.65  | 8.62  | 9.77  | 10.85 | 12.29 |
| Social support                                 | 2341    | 0.74        | 0.14       | 0.40  | 0.65  | 0.75  | 0.83  | 0.97  |
| Healthy life expectancy at birth               | 2309    | 64.42       | 8.34       | 48.00 | 58.00 | 64.00 | 71.00 | 83.00 |
| Freedom to make life choices                   | 2329    | 0.63        | 0.14       | 0.23  | 0.53  | 0.63  | 0.73  | 0.92  |
| Generosity                                     | 2285    | 0.04        | 0.17       | -0.24 | -0.00 | 0.01  | 0.05  | 0.57  |
| Perceptions of corruption                       | 2238    | 0.32        | 0.14       | 0.07  | 0.22  | 0.30  | 0.39  | 0.89  |
| Positive affect                                 | 2349    | 0.34        | 0.09       | 0.06  | 0.27  | 0.35  | 0.41  | 0.78  |
| Negative affect                                 | 2347    | 0.27        | 0.08       | 0.08  | 0.21  | 0.26  | 0.33  | 0.71  |

This table underscores the diverse aspects influencing happiness, particularly **Life Ladder** which has a mean score of approximately **5.41**, suggesting moderate happiness levels across countries surveyed. **Healthy life expectancy** also averages around **64.42 years**, indicating health as a crucial contributor to happiness perceptions.

## Categorical Column Overview

### Country_name

The **Country_name** column contains names of the countries involved in the survey. The dataset comprises a total of **2363 entries** spanning **165 unique countries**. Notably, **Argentina** has the highest frequency of entries, appearing **18 times**, which indicates its consistent representation in the dataset.

## Missing Values Analysis

Upon examination, the dataset does not exhibit missing values in categorical columns or the year column, indicating thorough data collection. However, some numerical columns have missing values:

| Column                                         | Percentage of Missing Values |
|------------------------------------------------|------------------------------|
| Log_GDP_per_capita                            | 1.18%                        |
| Social support                                 | 0.55%                        |
| Healthy life expectancy at birth               | 2.67%                        |
| Freedom to make life choices                   | 1.52%                        |
| Generosity                                     | 3.43%                        |
| Perceptions of corruption                       | 5.29%                        |
| Positive affect                                 | 1.02%                        |
| Negative affect                                 | 0.68%                        |

Despite some columns having missing values, the overall percentages are minimal, suggesting that the integrity of the dataset is largely intact.

![Missing Values](missing_values.png)

## Correlation Analysis

The correlation matrix indicates relationships between various numerical attributes. Key correlations include:

- **Life Ladder** is negatively correlated with **Negative affect** (-0.352) and positively correlated with **Positive affect** (not strong but positive at 0.334).
- **Social support** shows a significant negative correlation with **Negative affect** (-0.455), illustrating that individuals feeling more socially supported tend to experience fewer negative emotions.
- **Healthy life expectancy at birth** positively correlates with **Life Ladder** (0.168), suggesting that health is a contributing factor to happiness.

![Correlation Matrix](correlation_matrix.png)

## Visualizing Summary Statistics

The mean of the various numerical columns is compiled in a bar plot providing a visual representation of the averages impacting happiness perceptions across countries.

![Mean as Bar Plots](mean_as_bar_plots.png)

This visualization facilitates understanding which factors are perceived more positively than others. The **Life Ladder** and aspects like **Social support** and **Healthy life expectancy** show substantial averages, highlighting their importance.

## Distribution Analysis of Numerical Columns

Box plots provide an effective view into the distribution and spread of the numerical data, pinpointing outliers and variations within the columns.

![Boxplot of Numerical Columns](boxplot_num_cols.png)

From the box plot, we can see that while most numerical data follow a specific range, certain elements like **Generosity** have wider distributions with several outliers, indicating varying levels of generosity across countries.

## Insights and Implications

### Key Findings

1. **Social Support and Happiness**: Higher perceived social support correlates with lower negative affect and higher Life Ladder scores, pointing to the importance of community and relationship building in enhancing happiness.

2. **Economic Factors**: The relationship between **Log_GDP_per_capita** and happiness is weak (0.080), suggesting GDP alone is not a strong indicator of happiness. While economic conditions matter, they are not the sole contributors to individual well-being.

3. **Corruption Perception**: The perception of corruption positively correlates with negative affect (0.266). Countries with higher corruption perceptions experience reduced happiness levels.

### Recommendations

- **Policy Implications**: Governments should focus on improving social support systems, enhancing healthcare accessibility, and minimizing corruption. Programs aimed at strengthening community ties could significantly boost happiness metrics.

- **Further Analysis**: Future analyses could explore the relationship between these happiness indicators and external factors, such as education and occupation.

- **Data Quality Improvement**: Continuous monitoring for missing values, especially in the vital economic and social factors, would enhance the dataset's robustness.

## Conclusion

This comprehensive analysis of the happiness dataset underscores the multifaceted nature of happiness across nations. Understanding the correlations and insights derived from this data can empower policymakers, researchers, and community leaders to initiate positive changes conducive to elevating happiness and well-being in societies.

By leveraging the insights gained from these analyses, we can strive towards a healthier, more supportive, and happier world.
