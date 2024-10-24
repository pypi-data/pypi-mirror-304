#!/usr/bin/env python3
import argparse
import json
import sys
from typing import List, Dict, Any, Optional
from .owasp_checker import OWASPChecker

def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="OWASP Top Ten Compliance Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--url',
        type=str,
        help='URL to scan for vulnerabilities'
    )

    parser.add_argument(
        '--dependencies',
        type=str,
        help='Path to dependency file (requirements.txt, package.json, or pom.xml)'
    )

    parser.add_argument(
        '--vulnerability-types',
        type=str,
        nargs='+',
        help='Specific vulnerability types to scan for (e.g., sql_injection xss)'
    )

    parser.add_argument(
        '--output',
        type=str,
        choices=['json', 'text'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--output-file',
        type=str,
        help='Write output to file instead of stdout'
    )

    parser.add_argument(
        '--zap-proxy',
        type=str,
        default='http://localhost:8080',
        help='OWASP ZAP proxy address (default: http://localhost:8080)'
    )

    parser.add_argument(
        '--nvd-api-key',
        type=str,
        help='NVD API key for dependency checking'
    )

    parser.add_argument(
        '--vt-api-key',
        type=str,
        help='VirusTotal API key for threat intelligence'
    )

    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Enable test mode with mock responses'
    )

    return parser.parse_args()

def format_text_output(results: Dict[str, Any]) -> str:
    """Format results as human-readable text"""
    output = []
    
    # Format vulnerabilities
    output.append("=== Vulnerabilities ===")
    if 'vulnerabilities' in results:
        for vuln in results['vulnerabilities']:
            output.append(f"\nName: {vuln.get('name', 'Unknown')}")
            output.append(f"Risk: {vuln.get('risk', 'Unknown')}")
            output.append(f"Confidence: {vuln.get('confidence', 'Unknown')}")
            output.append(f"CVSS Score: {vuln.get('cvss_score', 'N/A')}")
            output.append(f"Description: {vuln.get('description', 'N/A')}")
            output.append(f"Solution: {vuln.get('solution', 'N/A')}")
            if 'exploitation_risk' in vuln:
                output.append(f"Exploitation Risk: {vuln['exploitation_risk']}")
            if 'active_exploits' in vuln:
                output.append(f"Active Exploits: {vuln['active_exploits']}")
    else:
        output.append("No vulnerabilities found.")

    # Format guidelines
    output.append("\n=== OWASP Guidelines ===")
    if 'guidelines' in results and 'OWASP Top Ten' in results['guidelines']:
        for category, description in results['guidelines']['OWASP Top Ten'].items():
            output.append(f"\n{category}:")
            output.append(description)
    else:
        output.append("No guidelines available.")

    return '\n'.join(output)

def write_output(results: Dict[str, Any], args: argparse.Namespace) -> None:
    """Write results to file or stdout"""
    # Format output
    output = (
        json.dumps(results, indent=2)
        if args.output == 'json'
        else format_text_output(results)
    )

    # Write output
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(output)
    else:
        print(output)

def main() -> int:
    """Main CLI function"""
    args = parse_args()

    # Validate arguments
    if not args.url and not args.dependencies:
        print("Error: Either --url or --dependencies must be specified")
        return 1

    try:
        # Initialize checker
        checker = OWASPChecker(
            zap_proxy_address=args.zap_proxy,
            nvd_api_key=args.nvd_api_key,
            vt_api_key=args.vt_api_key
        )

        # Enable test mode if requested
        if args.test_mode:
            checker.enable_test_mode()

        # Run security check
        results = checker.run_full_check(
            url=args.url,
            dependency_file=args.dependencies,
            vulnerability_types=args.vulnerability_types
        )

        # Write results
        write_output(results, args)
        return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 130
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
