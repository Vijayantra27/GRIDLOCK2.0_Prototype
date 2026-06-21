import "./globals.css";

export const metadata = {
  title: "GridLock AI",
  description: "AI Powered Parking Intelligence Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}