from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

# Add responsive state imports if not already present.
if "function useIsMobile" not in s:
    s = s.replace(
'''import { useEffect, useMemo, useState } from "react";''',
'''import { useEffect, useMemo, useState } from "react";'''
    )

# Add mobile state after status state.
old = '''  const [submitStatus, setSubmitStatus] = useState("Ready for AI system intake.");
'''
new = '''  const [submitStatus, setSubmitStatus] = useState("Ready for AI system intake.");
  const isMobile = useIsMobile();
'''
if old in s and new not in s:
    s = s.replace(old, new)

# Make main top-level sections responsive.
replacements = {
'''    <main style={styles.page}>''':
'''    <main style={responsive(styles.page, isMobile && styles.pageMobile)}>''',

'''        <header style={styles.hero}>''':
'''        <header style={responsive(styles.hero, isMobile && styles.heroMobile)}>''',

'''            <h1 style={styles.title}>SecureTheCloud AI Governance Board</h1>''':
'''            <h1 style={responsive(styles.title, isMobile && styles.titleMobile)}>SecureTheCloud AI Governance Board</h1>''',

'''          <div style={styles.doctrine}>''':
'''          <div style={responsive(styles.doctrine, isMobile && styles.doctrineMobile)}>''',

'''        <section style={styles.boundary}>''':
'''        <section style={responsive(styles.boundary, isMobile && styles.oneColumnGrid)}>''',

'''          <div style={styles.fabricGrid}>''':
'''          <div style={responsive(styles.fabricGrid, isMobile && styles.oneColumnGrid)}>''',

'''          <section style={styles.metrics}>''':
'''          <section style={responsive(styles.metrics, isMobile && styles.metricsMobile)}>''',

'''        <section style={styles.executive}>''':
'''        <section style={responsive(styles.executive, isMobile && styles.executiveMobile)}>''',

'''        <section style={styles.layerSection}>''':
'''        <section style={styles.layerSection}>''',

'''          <div style={styles.layerGrid}>''':
'''          <div style={responsive(styles.layerGrid, isMobile && styles.oneColumnGrid)}>''',

'''        <section style={styles.intakeGrid}>''':
'''        <section style={responsive(styles.intakeGrid, isMobile && styles.oneColumnGrid)}>''',

'''            <div style={styles.formGrid}>''':
'''            <div style={responsive(styles.formGrid, isMobile && styles.oneColumnGrid)}>''',

'''            <div style={styles.formGrid}>''':
'''            <div style={responsive(styles.formGrid, isMobile && styles.oneColumnGrid)}>''',

'''              <div style={styles.checkGrid}>''':
'''              <div style={responsive(styles.checkGrid, isMobile && styles.oneColumnGrid)}>''',

'''              <div style={styles.checkGrid}>''':
'''              <div style={responsive(styles.checkGrid, isMobile && styles.oneColumnGrid)}>''',

'''            <div style={styles.buttonRow}>''':
'''            <div style={responsive(styles.buttonRow, isMobile && styles.oneColumnGrid)}>''',

'''        <section style={styles.workspace}>''':
'''        <section style={responsive(styles.workspace, isMobile && styles.oneColumnGrid)}>''',

'''                  <div style={styles.detailGrid}>''':
'''                  <div style={responsive(styles.detailGrid, isMobile && styles.oneColumnGrid)}>''',

'''                <div style={styles.mappingGrid}>''':
'''                <div style={responsive(styles.mappingGrid, isMobile && styles.oneColumnGrid)}>'''
}

for old, new in replacements.items():
    s = s.replace(old, new)

# Make all fabric cards use mobile-safe min height if needed.
s = s.replace(
'''                <div key={name} style={{ ...styles.fabricCard, borderColor: color }}>''',
'''                <div key={name} style={{ ...responsive(styles.fabricCard, isMobile && styles.cardMobile), borderColor: color }}>'''
)

# Make layer cards stack more nicely on mobile.
s = s.replace(
'''              <div key={name} style={styles.layerCard}>''',
'''              <div key={name} style={responsive(styles.layerCard, isMobile && styles.layerCardMobile)}>'''
)

# Make panels mobile-safe.
s = s.replace(
'''          <div style={styles.panel}>''',
'''          <div style={responsive(styles.panel, isMobile && styles.panelMobile)}>'''
)

s = s.replace(
'''          <div style={{ ...styles.panel, ...styles.detailPanel }}>''',
'''          <div style={responsive({ ...styles.panel, ...styles.detailPanel }, isMobile && styles.panelMobile)}>'''
)

# Add helpers before Field component.
marker = '''function Field({
'''
helpers = '''function responsive(...items: Array<CSSProperties | false | null | undefined>): CSSProperties {
  return Object.assign({}, ...items.filter(Boolean));
}

function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const update = () => setIsMobile(window.innerWidth <= 820);
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  return isMobile;
}

'''
if "function responsive(" not in s:
    s = s.replace(marker, helpers + marker)

# Add mobile styles before footer style.
marker = '''  footer: {
'''
mobile_styles = '''  pageMobile: {
    padding: 12,
    overflowX: "hidden"
  },
  heroMobile: {
    flexDirection: "column",
    padding: 22
  },
  titleMobile: {
    fontSize: 40,
    lineHeight: 1
  },
  doctrineMobile: {
    minWidth: 0,
    width: "100%"
  },
  oneColumnGrid: {
    gridTemplateColumns: "1fr"
  },
  metricsMobile: {
    gridTemplateColumns: "repeat(2, minmax(0, 1fr))"
  },
  executiveMobile: {
    flexDirection: "column"
  },
  panelMobile: {
    padding: 18,
    width: "100%"
  },
  cardMobile: {
    minHeight: "auto"
  },
  layerCardMobile: {
    alignItems: "flex-start"
  },
'''
if "pageMobile:" not in s:
    s = s.replace(marker, mobile_styles + marker)

# Harden existing styles against overflow.
style_replacements = {
'''  shell: { maxWidth: 1500, margin: "0 auto" },''':
'''  shell: { maxWidth: 1500, margin: "0 auto", overflowX: "hidden" },''',

'''  badge: {
    border: "1px solid #38bdf8",''':
'''  badge: {
    border: "1px solid #38bdf8",
    maxWidth: "100%",
    overflowWrap: "anywhere",''',

'''    whiteSpace: "nowrap"''':
'''    whiteSpace: "normal"''',

'''  record: { border: "1px solid #334155", borderRadius: 16, padding: 16, background: "#020617", cursor: "pointer" },''':
'''  record: { border: "1px solid #334155", borderRadius: 16, padding: 16, background: "#020617", cursor: "pointer", overflowWrap: "anywhere" },''',

'''  selectedSystem: {
    border: "1px solid #22d3ee",''':
'''  selectedSystem: {
    border: "1px solid #22d3ee",
    overflowWrap: "anywhere",''',

'''  pill: {
    border: "1px solid #334155",''':
'''  pill: {
    border: "1px solid #334155",
    overflowWrap: "anywhere",'''
}

for old, new in style_replacements.items():
    s = s.replace(old, new)

# Add global mobile-safe CSS inside main.
old = '''    <main style={responsive(styles.page, isMobile && styles.pageMobile)}>'''
new = '''    <main style={responsive(styles.page, isMobile && styles.pageMobile)}>
      <style jsx global>{`
        * {
          box-sizing: border-box;
        }

        html,
        body {
          margin: 0;
          max-width: 100%;
          overflow-x: hidden;
        }

        input,
        select,
        textarea,
        button {
          max-width: 100%;
        }

        @media (max-width: 820px) {
          body {
            background: #020617;
          }
        }
      `}</style>'''
if old in s and "<style jsx global>" not in s:
    s = s.replace(old, new)

p.write_text(s)
