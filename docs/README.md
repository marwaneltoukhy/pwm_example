# Documentation Index

Welcome to the PWM Example project documentation!

## 📚 Available Documentation

### Getting Started
- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 30 minutes
  - Installation and setup
  - Running your first test
  - Modifying PWM parameters
  - Viewing waveforms

### Core Documentation
- **[Main README](../README.md)** - Project overview and main documentation
  - Features and specifications
  - Architecture overview
  - Memory map
  - Usage examples
  - Testing instructions
  - Physical implementation

- **[Project Dashboard](../PROJECT_DASHBOARD.md)** - Comprehensive project status
  - Executive summary
  - Component status matrix
  - Architecture diagrams
  - Technical analysis
  - Gap analysis and recommendations
  - Development roadmap
  - Quality metrics

### Technical Documentation
- **[Architecture Guide](ARCHITECTURE.md)** - Detailed system architecture
  - System hierarchy
  - Component descriptions
  - Bus architecture (Wishbone)
  - Memory organization
  - Interrupt architecture
  - Clock and reset strategy
  - Power architecture

- **[Testing Guide](TESTING_GUIDE.md)** - Complete testing documentation
  - Test infrastructure
  - Running tests (RTL, GL, GL+SDF)
  - Test descriptions and expected results
  - Debugging failed tests
  - Writing new tests
  - Continuous integration

### Reference Documentation
- **[Caravel Integration](source/index.md)** - Integration with Caravel platform
  - Caravel user project structure
  - OpenLane hardening flow
  - Timing analysis
  - Precheck requirements
  - Submission checklist

## 🎯 Where to Start?

**New to the project?**
→ Start with [Quick Start Guide](QUICK_START.md)

**Want to understand the design?**
→ Read [Main README](../README.md) and [Architecture Guide](ARCHITECTURE.md)

**Need to run tests?**
→ Check [Testing Guide](TESTING_GUIDE.md)

**Looking for project status?**
→ View [Project Dashboard](../PROJECT_DASHBOARD.md)

**Preparing for tapeout?**
→ Review [Caravel Integration](source/index.md) and dashboard checklist

## 📂 Documentation Structure

```
docs/
├── README.md                  # This file
├── QUICK_START.md            # Quick start guide
├── ARCHITECTURE.md           # Technical architecture
├── TESTING_GUIDE.md          # Testing documentation
└── source/
    ├── index.md              # Caravel integration guide
    ├── conf.py               # Sphinx configuration
    └── _static/              # Images and assets
```

## 🔄 Documentation Maintenance

This documentation is maintained alongside the code. When making changes:

1. **Update relevant docs** when modifying design
2. **Keep examples current** with actual code
3. **Update version numbers** in document footers
4. **Cross-reference** between documents for consistency

## 📝 Contributing to Documentation

To improve documentation:

1. Fork the repository
2. Edit markdown files in `docs/`
3. Test links and formatting
4. Submit pull request
5. Documentation will be reviewed with code changes

### Documentation Standards

- **Markdown format** for all docs
- **Clear headings** and table of contents
- **Code examples** that actually work
- **Screenshots/diagrams** where helpful
- **Version numbers** and last-updated dates

## 🔗 External Resources

### Caravel Platform
- [Caravel Repository](https://github.com/chipfoundry/caravel)
- [Caravel Documentation](https://caravel-sim-infrastructure.readthedocs.io/)

### IP Cores
- [CF_TMR32 Documentation](/nc/ip/CF_TMR32/)
- [CF_SRAM_1024x32 Documentation](/nc/ip/CF_SRAM_1024x32/)

### Tools
- [OpenLane Documentation](https://librelane.readthedocs.io/)
- [Cocotb Documentation](https://docs.cocotb.org/)
- [Wishbone Specification](https://opencores.org/howto/wishbone)
- [Sky130 PDK](https://skywater-pdk.readthedocs.io/)

### Learning Resources
- [Digital ASIC Design Basics](https://www.asic-world.com/)
- [Verilog Tutorial](https://www.chipverify.com/verilog/verilog-tutorial)
- [Cocotb Tutorial](https://docs.cocotb.org/en/stable/quickstart.html)

## 📞 Support

If you can't find what you need in the documentation:

- **Search** the documentation (Ctrl+F is your friend!)
- **Check examples** in the code (`verilog/dv/cocotb/user_proj_tests/`)
- **Browse issues** on GitHub
- **Ask questions** in Discussions
- **Contact maintainer** via email

---

**Documentation Version:** 1.0  
**Last Updated:** 2025-11-03  
**Maintained by:** PWM Example Project Team
