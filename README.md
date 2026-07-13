# Raspberry Pi Defensive Homelab

A practical defensive homelab project built around a Raspberry Pi 4 8GB and a 1TB SSD, focused on Linux, Docker, networking, monitoring, backups, hardening, logs, self-hosted services and Bitcoin security lessons.

This project is part of my cybersecurity portfolio and documents how I design, maintain, secure and improve a small home infrastructure environment with a Blue Team mindset.

## Main Goals

- Build and document a realistic self-hosted homelab.
- Practice Linux administration and Docker-based service management.
- Improve defensive security habits around logging, backups, updates and hardening.
- Document network architecture and service exposure.
- Apply Blue Team thinking to a real environment.
- Connect previous Bitcoin and Lightning node experience with operational security lessons.
- Create professional documentation useful for junior SOC / Blue Team roles.

## Hardware

- Raspberry Pi 4
- 8GB RAM
- 1TB SSD
- Home network environment

## Technical Areas

- Linux
- Docker
- Networking
- DNS filtering
- Backups
- Monitoring
- Logging
- Hardening
- Incident response notes
- Bitcoin and Lightning security lessons
- Self-hosted media services

## Services

Planned or documented services may include:

- AdGuard Home
- Jellyfin
- Jellyseerr
- Radarr
- Sonarr
- OpenVPN
- Monitoring tools
- Backup tooling
- Security logging tools

## Security Focus

This project is not only about running services. The main focus is understanding how to operate them safely:

- What is exposed?
- What needs authentication?
- What logs are available?
- What happens if a disk fails?
- How are backups handled?
- How are updates managed?
- What risks exist in a home network?
- What lessons apply to SOC and Blue Team work?

## Portfolio Purpose

This repository is designed to show practical, hands-on experience rather than only listing courses or certifications.

The goal is to demonstrate how I think, document, troubleshoot and improve systems over time.

## Status

Private preparation phase.

## Repository Structure

This repository is organized to make the homelab documentation easy to review, expand and sanitize before sharing publicly.

### Core Documentation

- [Project Overview](docs/project-overview.md) - Scope, safety rules and portfolio purpose.
- [Architecture](docs/architecture.md) - High-level system design, trust boundaries and placeholders.
- [Hardware](docs/hardware.md) - Hardware profile and operational considerations.
- [Network Layout](docs/network-layout.md) - Sanitized network layout and access rules.
- [Security Goals](docs/security-goals.md) - Defensive goals and recurring habits.
- [Roadmap](docs/roadmap.md) - Planned documentation, service and security improvements.

### Docker

- [Services](docker/services.md) - Service review template and planned Docker services.
- [Docker Compose Example](docker/docker-compose.example.yml) - Placeholder-only compose example.

### Security Operations

- [Hardening Checklist](security/hardening-checklist.md) - Host and Docker hardening starter checklist.
- [Logging and Monitoring](security/logging-and-monitoring.md) - Log sources, monitoring goals and TODOs.
- [Backup Strategy](security/backup-strategy.md) - Backup principles and planning table.
- [Incident Response Notes](security/incident-response-notes.md) - Sanitized incident note template.

### Bitcoin Security

- [Bitcoin Node Lessons](bitcoin-security/bitcoin-node-lessons.md) - Operational and defensive lessons.
- [Lightning Node Lessons](bitcoin-security/lightning-node-lessons.md) - Availability, backup and key management lessons.
- [OPSEC Notes](bitcoin-security/opsec-notes.md) - Repository privacy and secret-handling rules.

### Media Stack

- [AdGuard Home](media-stack/adguard.md) - DNS filtering defensive value and security notes.
- [Jellyfin](media-stack/jellyfin.md) - Media server defensive questions and TODOs.
- [Jellyseerr](media-stack/jellyseerr.md) - Request management security considerations.
- [Radarr and Sonarr](media-stack/radarr-sonarr.md) - Automation service risks and integration notes.
- [OpenVPN](media-stack/openvpn.md) - Remote access defensive value and key protection notes.
- [Media Stack Security Considerations](media-stack/security-considerations.md) - Shared risks and defensive practices.

### Assets

- [Diagrams Directory](assets/diagrams/) - Placeholder location for sanitized diagrams.
