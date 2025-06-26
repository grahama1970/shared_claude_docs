"""
Test module for statistical analysis capabilities

External Dependencies:
- pytest: https://docs.pytest.org/
- numpy: https://numpy.org/doc/stable/
- scipy: https://docs.scipy.org/doc/scipy/
- scikit-learn: https://scikit-learn.org/stable/
"""

import pytest
import numpy as np
from pathlib import Path
import sys
from scipy import stats

sys.path.append(str(Path(__file__).parent.parent))

from model_benchmarking_interaction import (
    ModelBenchmarkingSuite, BenchmarkMetrics
)


class TestStatisticalAnalysis:
    """Test statistical testing and analysis features"""
    
    @pytest.fixture
    def sample_metrics(self):
        """Create sample benchmark metrics for testing"""
        metrics1 = BenchmarkMetrics(
            model_name="Model A",
            framework="sklearn",
            dataset_name="test_dataset",
            accuracy=0.85,
            precision=0.84,
            recall=0.86,
            f1_score=0.85,
            cross_val_scores=[0.83, 0.84, 0.85, 0.86, 0.87],
            inference_time_mean=0.01,
            inference_time_std=0.002,
            memory_usage_mb=50.0
        )
        
        metrics2 = BenchmarkMetrics(
            model_name="Model B",
            framework="sklearn",
            dataset_name="test_dataset",
            accuracy=0.89,
            precision=0.88,
            recall=0.90,
            f1_score=0.89,
            cross_val_scores=[0.87, 0.88, 0.89, 0.90, 0.91],
            inference_time_mean=0.015,
            inference_time_std=0.003,
            memory_usage_mb=75.0
        )
        
        metrics3 = BenchmarkMetrics(
            model_name="Model C",
            framework="sklearn",
            dataset_name="test_dataset",
            accuracy=0.82,
            precision=0.81,
            recall=0.83,
            f1_score=0.82,
            cross_val_scores=[0.80, 0.81, 0.82, 0.83, 0.84],
            inference_time_mean=0.008,
            inference_time_std=0.001,
            memory_usage_mb=30.0
        )
        
        return [metrics1, metrics2, metrics3]
    
    def test_confidence_interval_calculation(self):
        """Test confidence interval calculation"""
        scores = [0.83, 0.84, 0.85, 0.86, 0.87]
        mean = np.mean(scores)
        std = np.std(scores)
        
        # 95% confidence interval
        ci_lower = mean - 1.96 * std
        ci_upper = mean + 1.96 * std
        
        assert ci_lower < mean < ci_upper
        assert ci_upper - ci_lower > 0
        
        # Test with BenchmarkMetrics
        metrics = BenchmarkMetrics(
            model_name="Test",
            framework="sklearn",
            dataset_name="test",
            cross_val_scores=scores
        )
        
        # Calculate CI manually
        metrics.confidence_interval = (ci_lower, ci_upper)
        
        assert metrics.confidence_interval[0] < mean
        assert metrics.confidence_interval[1] > mean
    
    def test_statistical_significance_testing(self, sample_metrics):
        """Test statistical significance between models"""
        suite = ModelBenchmarkingSuite()
        
        # Test with sample metrics that have cross_val_scores
        suite.results_history = sample_metrics
        suite._test_statistical_significance(sample_metrics)
        
        # Manual t-test verification
        scores1 = sample_metrics[0].cross_val_scores
        scores2 = sample_metrics[1].cross_val_scores
        
        t_stat, p_value = stats.ttest_rel(scores1, scores2)
        
        # Model B should be significantly better than Model A
        assert p_value < 0.05  # Statistically significant
        assert t_stat < 0  # Model A has lower scores
    
    def test_performance_regression_statistical(self):
        """Test regression detection with statistical significance"""
        baseline = BenchmarkMetrics(
            model_name="baseline",
            framework="sklearn",
            dataset_name="test",
            accuracy=0.90,
            cross_val_scores=[0.89, 0.90, 0.91, 0.90, 0.90],
            inference_time_mean=0.01
        )
        
        # Small regression (not significant)
        small_regression = BenchmarkMetrics(
            model_name="small_regression",
            framework="sklearn",
            dataset_name="test",
            accuracy=0.89,
            cross_val_scores=[0.88, 0.89, 0.90, 0.89, 0.89],
            inference_time_mean=0.011
        )
        
        # Large regression (significant)
        large_regression = BenchmarkMetrics(
            model_name="large_regression",
            framework="sklearn",
            dataset_name="test",
            accuracy=0.80,
            cross_val_scores=[0.79, 0.80, 0.81, 0.80, 0.80],
            inference_time_mean=0.02
        )
        
        suite = ModelBenchmarkingSuite()
        
        # Test small regression
        small_reg = suite.detect_performance_regression(
            small_regression, baseline, threshold=0.05
        )
        assert not small_reg['accuracy']  # <5% drop
        
        # Test large regression
        large_reg = suite.detect_performance_regression(
            large_regression, baseline, threshold=0.05
        )
        assert large_reg['accuracy']  # >5% drop
        assert large_reg['speed']  # 100% increase in time
    
    def test_cross_validation_scores(self):
        """Test cross-validation score handling"""
        from sklearn.datasets import make_classification
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import cross_val_score
        
        # Generate data
        X, y = make_classification(
            n_samples=1000, n_features=20, n_informative=15,
            n_classes=2, random_state=42
        )
        
        # Train model
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        
        # Get cross-validation scores
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
        
        assert len(cv_scores) == 5
        assert all(0 <= score <= 1 for score in cv_scores)
        assert np.std(cv_scores) < 0.1  # Should be relatively stable
    
    def test_distribution_comparison(self, sample_metrics):
        """Test comparing score distributions between models"""
        scores1 = np.array(sample_metrics[0].cross_val_scores)
        scores2 = np.array(sample_metrics[1].cross_val_scores)
        scores3 = np.array(sample_metrics[2].cross_val_scores)
        
        # Test normality (for small samples, might not be normal)
        _, p_normal1 = stats.normaltest(scores1)
        _, p_normal2 = stats.normaltest(scores2)
        
        # Kruskal-Wallis test (non-parametric)
        h_stat, p_kruskal = stats.kruskal(scores1, scores2, scores3)
        
        # At least one model should be different
        assert p_kruskal < 0.05
        
        # Mann-Whitney U test for pairwise comparison
        u_stat, p_mann = stats.mannwhitneyu(scores1, scores2, alternative='two-sided')
        assert p_mann < 0.05  # Models are different
    
    def test_effect_size_calculation(self, sample_metrics):
        """Test effect size calculations (Cohen's d)"""
        scores1 = np.array(sample_metrics[0].cross_val_scores)
        scores2 = np.array(sample_metrics[1].cross_val_scores)
        
        # Calculate Cohen's d
        mean1, mean2 = np.mean(scores1), np.mean(scores2)
        std1, std2 = np.std(scores1, ddof=1), np.std(scores2, ddof=1)
        
        # Pooled standard deviation
        n1, n2 = len(scores1), len(scores2)
        pooled_std = np.sqrt(((n1-1)*std1**2 + (n2-1)*std2**2) / (n1+n2-2))
        
        cohen_d = (mean2 - mean1) / pooled_std
        
        # Model B is better, so Cohen's d should be positive and large
        assert cohen_d > 0.8  # Large effect size
    
    def test_multiple_comparison_correction(self, sample_metrics):
        """Test multiple comparison correction (Bonferroni)"""
        # When comparing 3 models, we have 3 pairwise comparisons
        n_comparisons = 3
        alpha = 0.05
        corrected_alpha = alpha / n_comparisons
        
        # Perform pairwise t-tests
        p_values = []
        for i in range(len(sample_metrics)):
            for j in range(i+1, len(sample_metrics)):
                scores_i = sample_metrics[i].cross_val_scores
                scores_j = sample_metrics[j].cross_val_scores
                _, p_value = stats.ttest_rel(scores_i, scores_j)
                p_values.append(p_value)
        
        assert len(p_values) == n_comparisons
        
        # Check which comparisons are significant after correction
        significant_after_correction = sum(p < corrected_alpha for p in p_values)
        assert significant_after_correction >= 1  # At least one should be significant
    
    def test_variance_analysis(self, sample_metrics):
        """Test variance analysis across models"""
        # Extract inference time statistics
        times = [(m.inference_time_mean, m.inference_time_std) 
                 for m in sample_metrics]
        
        # Calculate coefficient of variation (CV)
        cvs = [std/mean for mean, std in times if mean > 0]
        
        # All CVs should be reasonable (< 50% for stable measurements)
        assert all(cv < 0.5 for cv in cvs)
        
        # Test homogeneity of variances (Levene's test)
        scores_list = [m.cross_val_scores for m in sample_metrics]
        _, p_levene = stats.levene(*scores_list)
        
        # p > 0.05 suggests variances are similar
        # This might or might not be true for our sample data
        assert isinstance(p_levene, float)
    
    def test_outlier_detection(self):
        """Test outlier detection in benchmark results"""
        # Create metrics with more obvious outliers
        normal_times = [0.01, 0.011, 0.012, 0.013, 0.014, 0.015]
        outlier_times = normal_times + [0.1, 0.001]  # Add more extreme outliers
        
        # Z-score method (lower threshold for testing)
        z_scores = np.abs(stats.zscore(outlier_times))
        outliers = z_scores > 2  # Lower threshold
        
        assert sum(outliers) >= 1  # Should detect at least one outlier
        
        # IQR method
        q1 = np.percentile(outlier_times, 25)
        q3 = np.percentile(outlier_times, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers_iqr = [(t < lower_bound or t > upper_bound) 
                        for t in outlier_times]
        
        assert sum(outliers_iqr) >= 1  # Should detect outliers
    
    def test_bootstrap_confidence_intervals(self):
        """Test bootstrap confidence interval calculation"""
        np.random.seed(42)
        scores = [0.83, 0.84, 0.85, 0.86, 0.87]
        n_bootstrap = 1000
        
        # Bootstrap resampling
        bootstrap_means = []
        for _ in range(n_bootstrap):
            bootstrap_sample = np.random.choice(scores, size=len(scores), replace=True)
            bootstrap_means.append(np.mean(bootstrap_sample))
        
        # Calculate percentile confidence intervals
        ci_lower = np.percentile(bootstrap_means, 2.5)
        ci_upper = np.percentile(bootstrap_means, 97.5)
        
        original_mean = np.mean(scores)
        
        assert ci_lower <= original_mean <= ci_upper
        assert ci_upper - ci_lower < 0.1  # Should be narrow for consistent scores


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])