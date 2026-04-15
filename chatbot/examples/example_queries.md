# Example Queries for Velero Chatbot

This document contains example queries you can use with the Velero Chatbot.

## General Velero Questions

### What is Velero?
```
What is Velero?
```

Expected answer: Overview of Velero as a Kubernetes backup and restore tool.

### Core Features
```
What are the main features of Velero?
```

```
What can I do with Velero?
```

## Installation and Setup

### Basic Installation
```
How do I install Velero?
```

```
What are the prerequisites for installing Velero?
```

### Cloud Provider Setup
```
How do I configure Velero for AWS?
```

```
What's the setup process for Velero on Azure?
```

```
How do I use Velero with Google Cloud Platform?
```

## Backup Operations

### Creating Backups
```
How do I create a backup in Velero?
```

```
What's the command to backup a specific namespace?
```

```
How can I backup only certain resources?
```

### Scheduled Backups
```
How do I schedule automatic backups?
```

```
What's the format for backup schedules?
```

```
Can I have multiple backup schedules?
```

### Backup Options
```
What backup options are available in Velero?
```

```
How do I include or exclude specific resources?
```

```
Can I backup persistent volumes?
```

## Restore Operations

### Basic Restore
```
How do I restore a backup?
```

```
What's the process for restoring to a different cluster?
```

### Selective Restore
```
Can I restore only specific resources from a backup?
```

```
How do I restore to a different namespace?
```

### Restore Scenarios
```
How do I restore after a disaster?
```

```
What's the best way to migrate a cluster using Velero?
```

## Advanced Topics

### Persistent Volume Snapshots
```
How does Velero handle persistent volume snapshots?
```

```
What's the difference between Restic and CSI snapshots?
```

### Hooks
```
What are backup hooks in Velero?
```

```
How do I configure restore hooks?
```

### Plugins
```
What plugins are available for Velero?
```

```
How do I install a custom plugin?
```

## Troubleshooting

### Common Issues
```
Why is my backup failing?
```

```
How do I debug Velero issues?
```

```
Where can I find Velero logs?
```

### Performance
```
How can I improve backup performance?
```

```
What affects restore speed?
```

## Architecture and Design

### How It Works
```
How does Velero architecture work?
```

```
What components make up Velero?
```

### Storage
```
What backup storage locations are supported?
```

```
How does Velero store backups?
```

## Integration

### Kubernetes Features
```
Does Velero support custom resources?
```

```
How does Velero handle cluster-scoped resources?
```

### Cloud Integration
```
Which cloud providers are supported?
```

```
Can I use Velero with on-premises storage?
```

## Best Practices

### Production Use
```
What are the best practices for using Velero in production?
```

```
How often should I schedule backups?
```

### Security
```
How does Velero handle security and encryption?
```

```
What permissions does Velero need?
```

## Migration Scenarios

### Cluster Migration
```
How do I migrate from one Kubernetes cluster to another?
```

```
Can I migrate between different cloud providers?
```

### Disaster Recovery
```
What's the disaster recovery process with Velero?
```

```
How do I set up a DR strategy using Velero?
```

## Comparison Questions

### vs Other Tools
```
How does Velero compare to other backup solutions?
```

```
What's the difference between Velero and native cloud backups?
```

## Configuration

### Settings
```
What configuration options are available?
```

```
How do I configure backup retention?
```

### Customization
```
Can I customize backup behavior?
```

```
How do I set backup storage location?
```

## Sample Conversation Flow

Here's an example of a natural conversation with the chatbot:

```
You: What is Velero?
Assistant: [Provides overview]

You: How do I install it?
Assistant: [Provides installation steps]

You: I'm using AWS, what do I need to configure?
Assistant: [Provides AWS-specific configuration]

You: Can you show me how to create a backup?
Assistant: [Provides backup command and options]

You: How do I schedule backups to run daily?
Assistant: [Provides schedule configuration]

You: What if I need to restore to a different namespace?
Assistant: [Provides restore with namespace mapping]
```

## Tips for Better Queries

1. **Be Specific:**
   - Good: "How do I backup a namespace called 'production'?"
   - Less Good: "How do I backup?"

2. **Include Context:**
   - Good: "I'm using AWS and want to configure S3 for Velero backups"
   - Less Good: "Configure storage"

3. **Ask Follow-ups:**
   - After getting an answer, you can ask related questions
   - The chatbot understands Velero context

4. **Use Natural Language:**
   - You can ask questions naturally
   - No need for specific keywords

## Testing the Chatbot

Use these queries to test different aspects:

1. **Factual Accuracy:**
   ```
   What version of Kubernetes does Velero support?
   ```

2. **Procedural Knowledge:**
   ```
   Walk me through the complete backup and restore process.
   ```

3. **Troubleshooting:**
   ```
   My backup is stuck in progress state, what should I check?
   ```

4. **Comparison:**
   ```
   When should I use Restic vs CSI snapshots?
   ```

5. **Edge Cases:**
   ```
   Can Velero backup CRDs and their instances?
   ```
