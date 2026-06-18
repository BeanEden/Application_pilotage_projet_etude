function exportToPDF() {
    const element = document.querySelector('.main-content');
    const pageTitle = document.title.split('—')[0].trim() || 'export';

    // Scroll to top to avoid clipping issues
    window.scrollTo(0, 0);

    // Create a loading overlay
    const loader = document.createElement('div');
    loader.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255,255,255,0.8);display:flex;justify-content:center;align-items:center;z-index:9999;font-weight:bold;color:var(--accent);';
    loader.innerHTML = '<div style="text-align:center;"><i class="ph-bold ph-spinner-gap" style="font-size:3rem;display:block;margin-bottom:10px;animation:spin 1s linear infinite;"></i>Génération du PDF en cours...</div>';
    document.body.appendChild(loader);

    // Add spin animation
    const styleSpin = document.createElement('style');
    styleSpin.innerHTML = '@keyframes spin { 100% { transform:rotate(360deg); } }';
    document.head.appendChild(styleSpin);

    // Hide buttons from export
    const buttons = element.querySelectorAll('button, .btn, .action-icons, .remove-btn, .edit-btn, .modal');
    buttons.forEach(b => b.style.display = 'none');

    // Configuration
    const opt = {
        margin: [10, 10, 10, 10],
        filename: `Vocalis_${pageTitle}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
            scale: 2,
            useCORS: true,
            letterRendering: true,
            scrollY: 0,
            scrollX: 0,
            x: 0,
            windowWidth: 900
        },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    };

    // Style adjustments for PDF
    const style = document.createElement('style');
    style.innerHTML = `
        .sidebar { display: none !important; }
        .main-content { 
            margin: 0 !important; 
            padding: 0 !important; 
            width: 100% !important; 
            max-width: 1100px !important; 
            left: 0 !important; 
            position: relative !important;
        }
        .card { break-inside: avoid; border: 1px solid #e5e5ea !important; box-shadow: none !important; margin-bottom: 15px !important; }
        .page-header { margin-bottom: 20px !important; }
        h1 { font-size: 24px !important; color: #1d1d1f !important; }
        .stat-card { border: 1px solid #e5e5ea !important; box-shadow: none !important; break-inside: avoid; }
        table { font-size: 9px !important; width: 100% !important; border-collapse: collapse !important; }
        th, td { padding: 5px !important; border-bottom: 1px solid #f2f2f7 !important; }
        .badge { border: 1px solid #eee !important; }
        canvas { max-width: 100% !important; height: auto !important; }
    `;
    document.head.appendChild(style);

    // Convert canvases to images for stability
    const canvases = element.querySelectorAll('canvas');
    const placeholders = [];
    canvases.forEach(canvas => {
        if (canvas.width > 0 && canvas.height > 0) {
            const img = document.createElement('img');
            try {
                img.src = canvas.toDataURL('image/png');
                img.style.width = canvas.offsetWidth + 'px';
                img.style.height = canvas.offsetHeight + 'px';
                canvas.parentNode.insertBefore(img, canvas);
                canvas.style.display = 'none';
                placeholders.push({ canvas, img });
            } catch (e) { console.warn('Canvas capture failed:', e); }
        }
    });

    // Run export
    html2pdf().set(opt).from(element).save().then(() => {
        // Restore visibility
        buttons.forEach(b => b.style.display = '');
        placeholders.forEach(p => {
            p.canvas.style.display = '';
            p.img.remove();
        });
        document.head.removeChild(style);
        document.head.removeChild(styleSpin);
        document.body.removeChild(loader);
    }).catch(err => {
        console.error('PDF Export Error:', err);
        document.body.removeChild(loader);
        alert('Erreur lors de la génération du PDF.');
    });
}
