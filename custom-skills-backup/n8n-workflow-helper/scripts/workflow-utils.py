#!/usr/bin/env python3
"""
n8n Workflow Utilities
Helper functions for common n8n workflow operations and debugging.
"""

import json
import requests
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class N8nWorkflowUtils:
    """Utility class for n8n workflow operations."""

    def __init__(self, base_url: str, api_key: str):
        """Initialize with n8n instance details."""
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'X-N8N-API-KEY': api_key,
            'Content-Type': 'application/json'
        }

    def list_workflows(self, active_only: bool = False) -> List[Dict]:
        """List all workflows with optional filtering."""
        url = f"{self.base_url}/rest/workflows"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Failed to list workflows: {response.text}")

        workflows = response.json().get('data', [])

        if active_only:
            workflows = [w for w in workflows if w.get('active', False)]

        return workflows

    def get_workflow_json(self, workflow_id: str) -> Dict:
        """Get complete workflow JSON by ID."""
        url = f"{self.base_url}/rest/workflows/{workflow_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Failed to get workflow: {response.text}")

        return response.json()

    def export_workflow(self, workflow_id: str, filename: Optional[str] = None) -> str:
        """Export workflow to JSON file."""
        workflow = self.get_workflow_json(workflow_id)

        if not filename:
            name = workflow.get('name', f'workflow_{workflow_id}')
            # Sanitize filename
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)

        return filename

    def validate_workflow(self, workflow_json: Dict) -> Dict:
        """Validate workflow structure and connections."""
        issues = []

        # Check required fields
        required_fields = ['name', 'nodes', 'connections']
        for field in required_fields:
            if field not in workflow_json:
                issues.append(f"Missing required field: {field}")

        if 'nodes' in workflow_json:
            nodes = workflow_json['nodes']
            if not isinstance(nodes, list):
                issues.append("Nodes must be a list")
            else:
                # Check for duplicate node IDs
                node_ids = [node.get('id') for node in nodes]
                duplicates = set([x for x in node_ids if node_ids.count(x) > 1])
                if duplicates:
                    issues.append(f"Duplicate node IDs found: {duplicates}")

                # Check for nodes without IDs
                nodes_without_ids = [node for node in nodes if not node.get('id')]
                if nodes_without_ids:
                    issues.append(f"Nodes without IDs: {len(nodes_without_ids)}")

        if 'connections' in workflow_json:
            connections = workflow_json['connections']
            if not isinstance(connections, dict):
                issues.append("Connections must be a dictionary")

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'node_count': len(workflow_json.get('nodes', [])),
            'connection_count': len(workflow_json.get('connections', {}))
        }

    def analyze_workflow_performance(self, workflow_id: str, days: int = 7) -> Dict:
        """Analyze workflow execution performance over time."""
        # This would require execution history access
        # Implementation depends on available n8n APIs

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Placeholder for execution analysis
        return {
            'workflow_id': workflow_id,
            'analysis_period': f"{start_date.date()} to {end_date.date()}",
            'metrics': {
                'total_executions': 0,
                'success_rate': 0.0,
                'average_duration': 0.0,
                'error_rate': 0.0
            }
        }

    def backup_all_workflows(self, output_dir: str = "./backups") -> List[str]:
        """Backup all active workflows to specified directory."""
        import os
        os.makedirs(output_dir, exist_ok=True)

        workflows = self.list_workflows(active_only=True)
        backed_up_files = []

        for workflow in workflows:
            try:
                filename = self.export_workflow(workflow['id'], None)
                # Move to backup directory
                backup_path = os.path.join(output_dir, os.path.basename(filename))
                os.rename(filename, backup_path)
                backed_up_files.append(backup_path)
                print(f"✅ Backed up: {workflow['name']}")

            except Exception as e:
                print(f"❌ Failed to backup {workflow['name']}: {e}")

        return backed_up_files

    def find_broken_connections(self, workflow_json: Dict) -> List[str]:
        """Find broken or invalid connections in workflow."""
        issues = []
        nodes = {node['id']: node for node in workflow_json.get('nodes', [])}
        connections = workflow_json.get('connections', {})

        for source_node_id, source_connections in connections.items():
            if source_node_id not in nodes:
                issues.append(f"Connection from non-existent node: {source_node_id}")
                continue

            for connection_type, targets in source_connections.items():
                if not isinstance(targets, list):
                    issues.append(f"Invalid connection format for {source_node_id}.{connection_type}")
                    continue

                for target_list in targets:
                    if not isinstance(target_list, list) or len(target_list) < 2:
                        issues.append(f"Invalid target format in {source_node_id}.{connection_type}")
                        continue

                    target_node_id = target_list[0]
                    if target_node_id not in nodes:
                        issues.append(f"Connection to non-existent node: {target_node_id}")

        return issues


def main():
    """Command-line interface for workflow utilities."""
    import argparse

    parser = argparse.ArgumentParser(description='n8n Workflow Utilities')
    parser.add_argument('--url', required=True, help='n8n instance URL')
    parser.add_argument('--key', required=True, help='n8n API key')
    parser.add_argument('command', choices=['list', 'export', 'validate', 'backup'])
    parser.add_argument('--workflow-id', help='Workflow ID for export/validate')
    parser.add_argument('--output-dir', default='./backups', help='Output directory for backups')

    args = parser.parse_args()

    utils = N8nWorkflowUtils(args.url, args.key)

    try:
        if args.command == 'list':
            workflows = utils.list_workflows()
            print(f"Found {len(workflows)} workflows:")
            for wf in workflows:
                status = "🟢 ACTIVE" if wf.get('active') else "🔴 INACTIVE"
                print(f"  {wf['id']}: {wf['name']} - {status}")

        elif args.command == 'export':
            if not args.workflow_id:
                print("❌ --workflow-id required for export")
                return
            filename = utils.export_workflow(args.workflow_id)
            print(f"✅ Exported to: {filename}")

        elif args.command == 'validate':
            if not args.workflow_id:
                print("❌ --workflow-id required for validation")
                return
            workflow = utils.get_workflow_json(args.workflow_id)
            result = utils.validate_workflow(workflow)
            print(f"Validation for '{workflow['name']}':")
            print(f"  Valid: {result['valid']}")
            print(f"  Nodes: {result['node_count']}")
            print(f"  Connections: {result['connection_count']}")
            if result['issues']:
                print("  Issues:")
                for issue in result['issues']:
                    print(f"    ❌ {issue}")

        elif args.command == 'backup':
            files = utils.backup_all_workflows(args.output_dir)
            print(f"✅ Backed up {len(files)} workflows to {args.output_dir}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
