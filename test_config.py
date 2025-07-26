from src.config import Config, setup_logging

# Test configuration loading
def test_configuration():
    # Setup logging
    logger = setup_logging()
    logger.info("Testing configuration system...")
    
    # Load configuration
    config = Config()
    
    # Test risk thresholds
    print("Risk Thresholds:")
    print(f"  Low Risk: {config.risk_thresholds['low_risk']}")
    print(f"  Medium Risk: {config.risk_thresholds['medium_risk']}")
    print(f"  High Risk: {config.risk_thresholds['high_risk']}")
    
    # Test risk weights
    print("\nRisk Weights:")
    for factor, weight in config.risk_weights.items():
        print(f"  {factor}: {weight}")
    
    # Test data paths
    print(f"\nData Paths:")
    print(f"  Raw: {config.data_paths['raw_path']}")
    print(f"  Processed: {config.data_paths['processed_path']}")
    
    logger.info("Configuration test completed successfully!")

if __name__ == "__main__":
    test_configuration()