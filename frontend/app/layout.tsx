export const metadata = {
  title: "SecureTheCloud AI Governance Board",
  description: "Simulated enterprise AI governance review board platform"
};

export const viewport = {
  width: "device-width",
  initialScale: 1
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
