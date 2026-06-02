export const metadata = {
  title: "SecureTheCloud AI Governance Board",
  description: "Simulated enterprise AI governance review board platform"
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
