import React from 'react';

function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="px-6 py-4">
          <h1 className="text-xl font-semibold">Prepa 25 - Sistema de Evaluación</h1>
        </div>
      </header>
      <main className="p-6">
        {children}
      </main>
    </div>
  );
}

export default Layout;