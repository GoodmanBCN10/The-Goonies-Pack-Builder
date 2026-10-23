const I18N = {
  es: {
    heroTagline:
      "Crea tu pack personalizado de The Goonies OS, selecciona tus aplicaciones homebrew favoritas e instálalo directamente en tu Nintendo Switch mediante USB.",
    pillFw: "FIRMWARE OBJETIVO",
    pillFwTitle: "Versión del sistema oficial de la consola para la que se ajustarán las apps",
    pillAtmoTitle:
      "Atmosphere: Es el Custom Firmware (sistema modificado) que permite ejecutar homebrew en la Switch",
    pillHekateTitle:
      "Hekate: Es el menú de arranque inicial desde el que conectas la microSD por USB al PC y lanzas el sistema",
    btnGlossary: "Glosario / Ayuda",
    syncChecking: "🔄 Comprobando GitHub...",
    syncNormal: "🔄 Sincronizar GitHub",
    syncUpdates: (n) => `🔄 GitHub (${n} novedad${n > 1 ? "es" : ""})`,
    syncTooltipUpdates: (list) =>
      `Se han detectado y cargado nuevas versiones automáticamente:\n- ${list.join("\n- ")}`,
    syncTooltipOk: "Catálogo sincronizado con las últimas versiones de GitHub",
    presetsLabel: "Perfil rápido:",
    presetRec: "Recomendado",
    presetRecTitle:
      "Selección recomendada (MissionControl, Nextendo, Quick Reboot, 90DNS Setter y 90DNS Tester)",
    presetMin: "Mínimo (Básico)",
    presetMinTitle: "Solo el sistema CFW base con lo imprescindible",
    presetFull: "Completo (Todo)",
    presetFullTitle: "Selecciona todas las aplicaciones y herramientas disponibles",
    step1Title: "1. Versión de Firmware y Sistema Base (The Goonies OS)",
    compatBadge: "Compatibilidad Automática Activa",
    incompatTitle: "⚠️ Aviso de Incompatibilidad:",
    incompatMsg: (tag, atmo, maxFw, targetFw) =>
      `El Pack Base ${tag} (Atmosphere ${atmo}) solo soporta hasta el Firmware ${maxFw}, pero has seleccionado el Firmware ${targetFw}. La consola no arrancará si el firmware supera al soportado por Atmosphere.`,
    labelFwSelect: "Versión de Firmware para tu Consola",
    tipFwSelect:
      "Elige el último Firmware (23.0.1) salvo que quieras mantener tu consola en una versión antigua específica.",
    fwHelp:
      "Las aplicaciones se ajustan automáticamente a la versión compatible con el Firmware que elijas aquí.",
    chkIncludeFwHtml:
      'Copiar carpeta <code>/Firmware X.Y.Z</code> a la microSD (para actualizar con <strong>Daybreak</strong> <span class="info-dot">?</span>)',
    chkIncludeFwTitle:
      "Daybreak es el instalador incluido en tu Switch para actualizar el firmware desde la propia microSD sin conectar con Nintendo.",
    labelBaseSelect: "Pack CFW Base (The Goonies OS)",
    tipBaseSelect: "Contiene Atmosphere, Hekate, The Goonies App y DBI en Castellano.",
    latestDefaultSuffix: " (Último - Por defecto)",
    autoBaseOption: "Automático según Firmware elegido",
    baseSelectedLabel: "Seleccionado:",
    baseSupportsUpTo: "Soporta Firmware hasta",
    baseSizeLabel: "Tamaño:",
    cachedBadge: "⚡ En caché",
    cachedTitle: "Ya descargado en la caché de tu PC",
    step2Title: "2. Aplicaciones y Funciones Extras",
    gridExplainerHtml:
      "💡 <strong>¿Qué se instalará?</strong> Tu consola quedará exactamente con las aplicaciones que dejes <strong>marcadas</strong> abajo (además de <em>The Goonies App</em> y <em>DBI en Castellano</em>, que van siempre incluidas en el sistema base).",
    searchPlaceholder: "🔍 Buscar aplicación (ej. mandos, partidas, dns...)",
    catAll: "Todas",
    catSys: "Sistema / Mandos",
    catInst: "Instaladores / Menú",
    catNet: "Online / Red",
    catSave: "Partidas / Cuentas",
    emptySearch: "No hay aplicaciones que coincidan con tu búsqueda o filtro.",
    badgeInstall: "✓ Se instalará",
    badgeInstallTitle: "Marcada: se instalará en tu microSD",
    badgeSkip: "No instalar",
    badgeSkipTitle: "Desmarcada: no se instalará en la consola",
    badgeBaseDefault: "Ya en Pack Base",
    badgeBaseTitle: "El Pack Base ya incluye esta herramienta y la conservará",
    versionPrefix: "Versión:",
    step3Title: "3. Payloads de Arranque (Hekate)",
    tipPayloads:
      "Los Payloads son utilidades que se abren desde el menú 'Payloads' de Hekate antes de arrancar el sistema normal.",
    step3SubHtml:
      "El Pack Base ya incluye los payloads esenciales (<code>fusee.bin</code> y <code>Lockpick RCM Pro</code>) en <code>/bootloader/payloads/</code>.",
    usbPanelTitle: "Conexión con la Consola (Hekate USB)",
    hekateGuideTitle: "🔌 Cómo conectar tu Switch en 3 pasos:",
    hekateStep1Html: "Enciende la consola en el menú <strong>Hekate</strong>.",
    hekateStep2Html: "Toca en <code>Tools</code> &rarr; <code>USB Tools</code> &rarr; <code>SD Card</code>.",
    hekateStep3Html: "Conecta el cable USB al PC y verás tu microSD abajo.",
    sdDriveLabel: "Unidad microSD / Consola detectada",
    btnRefreshSd: "Detectar SD",
    btnExploreSd: "Explorar",
    btnEjectSd: "Desconectar Consola",
    ejectingText: "⏳ Expulsando...",
    noSdDetectedOpt: "— Ninguna consola / microSD detectada por USB —",
    noSdStatusHtml:
      "⚠️ Conecta la Switch en <strong>Hekate &rarr; Tools &rarr; USB Tools &rarr; SD Card</strong>.",
    sdFreeOfTotal: (free, total) => `${free} GB libres de ${total} GB`,
    sdDetectedBadges: (b) => `Detectado: <strong>${b}</strong>`,
    sdReadyClean: "Unidad lista para instalación limpia",
    sdConnectedIn: "Conectada en",
    lblSumBase: "Pack CFW Base:",
    lblSumFw: "Carpeta Firmware:",
    noFwFolder: (fw) => `Sin carpeta FW (Target ${fw})`,
    lblSumApps: "Apps / Payloads marcados:",
    lblSumTotal: "📦 Total a instalar en SD:",
    lblSumCached: "⚡ Ya en caché (en tu PC):",
    lblSumDownload: "⬇️ Pendiente de descargar:",
    allInCache: "0 MB (¡Todo en caché!)",
    treeTitle: "Qué se instalará en tu microSD",
    treeKeepProtected: "🛡️ Se conservan intactas: emuMMC y Nintendo",
    treeBasePack: (tag) => `📦 Sistema Base: The Goonies OS ${tag}`,
    treeFwDaybreak: (v) => `💿 Firmware ${v} listo para Daybreak`,
    treeInBaseSuffix: "(incluido en Base)",
    cacheInfo: (mb, count) => `Archivos guardados en caché: ${mb} MB (${count})`,
    btnClearCache: "Vaciar caché",
    btnBuild: "INSTALAR PACK EN LA CONSOLA (SD)",
    statusWaiting: "Esperando orden de instalación",
    confirmModalTitle: "⚠️ Aviso de Instalación Limpia en la microSD",
    confirmLeadHtml: (drv) =>
      `Estás a punto de instalar <strong>The Goonies OS</strong> en la unidad <strong>${drv}</strong>`,
    confirmDetailHtml:
      "Se realizará una <strong>instalación limpia</strong>: se eliminarán <strong>TODAS las carpetas y archivos</strong> existentes en la raíz de la microSD <strong>EXCEPTO</strong> las carpetas:",
    pillEmummc: "🛡️ emuMMC (Intacta)",
    pillNintendo: "🛡️ Nintendo (Intacta)",
    confirmNote:
      "Nota: Todas las descargas necesarias se verificarán primero en tu PC antes de borrar ningún archivo de la microSD. No desconectes el cable USB hasta que el proceso llegue al 100%.",
    btnCancel: "Cancelar",
    btnAcceptConfirm: "✅ Sí, hacer instalación limpia ahora",
    alertNoSd:
      "No se ha detectado ninguna unidad microSD seleccionada.\n\nPor favor, conecta tu Switch en Hekate -> Tools -> USB Tools -> SD Card y pulsa '🔄 Detectar SD'.",
    alertIncompatConfirm: (msg) =>
      `⚠️ ADVERTENCIA DE INCOMPATIBILIDAD:\n\n${msg}\n\n¿Seguro que deseas continuar de todos modos?`,
    glossaryModalTitle: "📘 Guía Rápida y Glosario para Usuarios Nuevos",
    btnOkGlossary: "¡Entendido!",
    glossaryItems: [
      {
        title: "🚀 Hekate (Bootloader)",
        desc: "Es el menú táctil que aparece al encender la consola modificada. Sirve para conectar la tarjeta microSD al PC por cable USB (Tools → USB Tools → SD Card) y para arrancar el sistema.",
      },
      {
        title: "🌌 Atmosphere (CFW)",
        desc: "Es el sistema modificado (Custom Firmware) donde juegas y usas aplicaciones Homebrew. Cada versión de Atmosphere soporta hasta una versión máxima de Firmware de Nintendo.",
      },
      {
        title: "🛡️ emuMMC y Carpeta Nintendo",
        desc: "emuMMC es la copia virtual segura de la memoria de tu consola dentro de la microSD, y Nintendo contiene tus juegos instalados y capturas. Este programa las protege siempre y nunca las borra.",
      },
      {
        title: "💿 Daybreak (Actualizar Firmware)",
        desc: "Es una aplicación incluida en tu menú Homebrew que instala la carpeta /Firmware X.Y.Z que este programa copia en tu microSD, permitiéndote actualizar la consola de forma 100% segura y offline.",
      },
      {
        title: "🧩 Sysmodules y Overlays (MissionControl / Ultrahand)",
        desc: "Son mejoras que funcionan en segundo plano mientras juegas: por ejemplo, conectar mandos de PS4/PS5/Xbox por Bluetooth (MissionControl) o abrir un menú lateral pulsando L + Abajo + R3 (Ultrahand).",
      },
      {
        title: "🔑 Payloads (Lockpick RCM Pro)",
        desc: "Son pequeñas herramientas (archivos .bin) que se abren desde el botón Payloads dentro de Hekate, por ejemplo para extraer las claves (keys) de tu consola.",
      },
    ],
  },
  en: {
    heroTagline:
      "Create your custom The Goonies OS pack, select your favorite homebrew apps and install it directly onto your Nintendo Switch via USB.",
    pillFw: "TARGET FIRMWARE",
    pillFwTitle: "Official console system version for which compatible apps will be selected",
    pillAtmoTitle:
      "Atmosphere: The Custom Firmware (modified OS) that enables homebrew on the Nintendo Switch",
    pillHekateTitle:
      "Hekate: The initial bootloader menu used to mount the microSD via USB to your PC and launch the OS",
    btnGlossary: "Glossary / Help",
    syncChecking: "🔄 Checking GitHub...",
    syncNormal: "🔄 Sync GitHub",
    syncUpdates: (n) => `🔄 GitHub (${n} new)`,
    syncTooltipUpdates: (list) =>
      `New releases were automatically found and loaded:\n- ${list.join("\n- ")}`,
    syncTooltipOk: "Catalog is up to date with the latest GitHub releases",
    presetsLabel: "Quick Profile:",
    presetRec: "Recommended",
    presetRecTitle:
      "Recommended selection (MissionControl, Nextendo, Quick Reboot, 90DNS Setter & 90DNS Tester)",
    presetMin: "Minimal (Basic)",
    presetMinTitle: "Only the essential base CFW system without extras",
    presetFull: "Full (Everything)",
    presetFullTitle: "Selects all available applications and tools",
    step1Title: "1. Firmware Version & Base System (The Goonies OS)",
    compatBadge: "Auto-Compatibility Active",
    incompatTitle: "⚠️ Incompatibility Warning:",
    incompatMsg: (tag, atmo, maxFw, targetFw) =>
      `Base Pack ${tag} (Atmosphere ${atmo}) only supports up to Firmware ${maxFw}, but you selected Firmware ${targetFw}. The console will not boot if the firmware exceeds Atmosphere's supported version.`,
    labelFwSelect: "Target Console Firmware Version",
    tipFwSelect:
      "Choose the latest Firmware (23.0.1) unless you want to keep your console on a specific older version.",
    fwHelp:
      "Applications are automatically matched to the latest version compatible with the Firmware selected here.",
    chkIncludeFwHtml:
      'Copy <code>/Firmware X.Y.Z</code> folder to microSD (to update with <strong>Daybreak</strong> <span class="info-dot">?</span>)',
    chkIncludeFwTitle:
      "Daybreak is the built-in Switch homebrew app used to install firmware updates directly from the microSD offline.",
    labelBaseSelect: "Base CFW Pack (The Goonies OS)",
    tipBaseSelect: "Contains Atmosphere, Hekate, The Goonies App and Spanish DBI.",
    latestDefaultSuffix: " (Latest - Default)",
    autoBaseOption: "Automatic based on chosen Firmware",
    baseSelectedLabel: "Selected:",
    baseSupportsUpTo: "Supports Firmware up to",
    baseSizeLabel: "Size:",
    cachedBadge: "⚡ Cached",
    cachedTitle: "Already downloaded in your PC cache",
    step2Title: "2. Extra Applications & Features",
    gridExplainerHtml:
      "💡 <strong>What will be installed?</strong> Your console will have the exact applications you leave <strong>checked</strong> below (plus <em>The Goonies App</em> and <em>Spanish DBI</em>, which are always included in the base system).",
    searchPlaceholder: "🔍 Search app (e.g. controllers, saves, dns...)",
    catAll: "All",
    catSys: "System / Controllers",
    catInst: "Installers / Menu",
    catNet: "Online / Network",
    catSave: "Saves / Accounts",
    emptySearch: "No applications match your search or category filter.",
    badgeInstall: "✓ Will install",
    badgeInstallTitle: "Checked: will be installed onto your microSD",
    badgeSkip: "Skip",
    badgeSkipTitle: "Unchecked: will not be installed",
    badgeBaseDefault: "In Base Pack",
    badgeBaseTitle: "The Base Pack already includes this tool and will keep it intact",
    versionPrefix: "Version:",
    step3Title: "3. Boot Payloads (Hekate)",
    tipPayloads:
      "Payloads are utilities launched from Hekate's 'Payloads' menu before booting the normal OS.",
    step3SubHtml:
      "The Base Pack already includes the essential payloads (<code>fusee.bin</code> and <code>Lockpick RCM Pro</code>) inside <code>/bootloader/payloads/</code>.",
    usbPanelTitle: "Console Connection (Hekate USB)",
    hekateGuideTitle: "🔌 How to connect your Switch in 3 steps:",
    hekateStep1Html: "Boot your console into the <strong>Hekate</strong> menu.",
    hekateStep2Html: "Tap <code>Tools</code> &rarr; <code>USB Tools</code> &rarr; <code>SD Card</code>.",
    hekateStep3Html: "Plug the USB cable into your PC and your microSD will appear below.",
    sdDriveLabel: "Detected microSD / Console Drive",
    btnRefreshSd: "Detect SD",
    btnExploreSd: "Browse",
    btnEjectSd: "Disconnect Console",
    ejectingText: "⏳ Ejecting...",
    noSdDetectedOpt: "— No console / microSD detected via USB —",
    noSdStatusHtml:
      "⚠️ Connect your Switch in <strong>Hekate &rarr; Tools &rarr; USB Tools &rarr; SD Card</strong>.",
    sdFreeOfTotal: (free, total) => `${free} GB free of ${total} GB`,
    sdDetectedBadges: (b) => `Detected: <strong>${b}</strong>`,
    sdReadyClean: "Drive ready for clean installation",
    sdConnectedIn: "Connected on",
    lblSumBase: "Base CFW Pack:",
    lblSumFw: "Firmware Folder:",
    noFwFolder: (fw) => `No FW folder (Target ${fw})`,
    lblSumApps: "Checked Apps / Payloads:",
    lblSumTotal: "📦 Total to install on SD:",
    lblSumCached: "⚡ Already cached (on PC):",
    lblSumDownload: "⬇️ Remaining to download:",
    allInCache: "0 MB (All cached!)",
    treeTitle: "What will be installed on your microSD",
    treeKeepProtected: "🛡️ Kept untouched: emuMMC & Nintendo",
    treeBasePack: (tag) => `📦 Base System: The Goonies OS ${tag}`,
    treeFwDaybreak: (v) => `💿 Firmware ${v} ready for Daybreak`,
    treeInBaseSuffix: "(included in Base)",
    cacheInfo: (mb, count) => `Cached files on PC: ${mb} MB (${count})`,
    btnClearCache: "Clear cache",
    btnBuild: "INSTALL PACK TO CONSOLE (SD)",
    statusWaiting: "Waiting for install command",
    confirmModalTitle: "⚠️ Clean Installation Warning (microSD)",
    confirmLeadHtml: (drv) =>
      `You are about to install <strong>The Goonies OS</strong> onto drive <strong>${drv}</strong>`,
    confirmDetailHtml:
      "A <strong>clean installation</strong> will be performed: <strong>ALL existing folders and files</strong> in the root of the microSD will be deleted <strong>EXCEPT</strong> the folders:",
    pillEmummc: "🛡️ emuMMC (Untouched)",
    pillNintendo: "🛡️ Nintendo (Untouched)",
    confirmNote:
      "Note: All required downloads are verified on your PC first before deleting any file on the microSD. Do not unplug the USB cable until progress reaches 100%.",
    btnCancel: "Cancel",
    btnAcceptConfirm: "✅ Yes, perform clean install now",
    alertNoSd:
      "No microSD drive is selected.\n\nPlease connect your Switch in Hekate -> Tools -> USB Tools -> SD Card and click '🔄 Detect SD'.",
    alertIncompatConfirm: (msg) =>
      `⚠️ INCOMPATIBILITY WARNING:\n\n${msg}\n\nAre you sure you want to proceed anyway?`,
    glossaryModalTitle: "📘 Quick Guide & Glossary for New Users",
    btnOkGlossary: "Got it!",
    glossaryItems: [
      {
        title: "🚀 Hekate (Bootloader)",
        desc: "The touch menu that appears when turning on your modded console. It lets you mount the microSD card to your PC via USB cable (Tools → USB Tools → SD Card) and boot the system.",
      },
      {
        title: "🌌 Atmosphere (CFW)",
        desc: "The Custom Firmware (modified OS) where you play games and run Homebrew apps. Each version of Atmosphere supports up to a specific maximum Nintendo Firmware version.",
      },
      {
        title: "🛡️ emuMMC & Nintendo Folder",
        desc: "emuMMC is the safe virtual copy of your console's internal memory stored on the microSD, and Nintendo holds your installed games and screenshots. This tool always protects them and never deletes them.",
      },
      {
        title: "💿 Daybreak (Firmware Updater)",
        desc: "A homebrew app included in your Homebrew Menu that installs the /Firmware X.Y.Z folder copied to your microSD, letting you update your console 100% safely and offline.",
      },
      {
        title: "🧩 Sysmodules & Overlays (MissionControl / Ultrahand)",
        desc: "Background enhancements that work while playing: for instance, connecting PS4/PS5/Xbox Bluetooth controllers (MissionControl) or opening a side overlay menu by pressing L + DPad Down + R3 (Ultrahand).",
      },
      {
        title: "🔑 Payloads (Lockpick RCM Pro)",
        desc: "Small boot utilities (.bin files) launched from the Payloads menu inside Hekate—for example, to dump your console's encryption keys.",
      },
    ],
  },
};

const state = {
  lang: "es",
  targetFirmware: "",
  basePackTag: "",
  userChangedFw: false,
  userChangedBase: false,
  ghSyncApplied: false,
  includeFirmwareFiles: true,
  selectedApps: new Set(),
  selectedPayloads: new Set(),
  customVersions: {},
  catalogData: null,
  initializedDefaults: false,
  selectedDrive: "",
  sdDrives: [],
  pollTimer: null,
  driveAutoTimer: null,
  searchQuery: "",
  categoryFilter: "all",
  activePreset: "recommended",
};

function t() {
  return I18N[state.lang] || I18N.es;
}

function getItemName(item) {
  return state.lang === "en" && item.name_en ? item.name_en : item.name || "";
}

function getItemCategory(item) {
  return state.lang === "en" && item.category_en ? item.category_en : item.category || "Homebrew";
}

function getItemDesc(item) {
  return state.lang === "en" && item.description_en ? item.description_en : item.description || "";
}

function getItemBaseBadge(item) {
  if (state.lang === "en" && item.base_badge_text_en) return item.base_badge_text_en;
  return item.base_badge_text || t().badgeBaseDefault;
}

function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function formatMB(bytes) {
  if (!bytes || bytes <= 0) return "0 MB";
  const mb = bytes / (1024 * 1024);
  return (mb < 0.1 ? 0.1 : mb).toFixed(1) + " MB";
}

function matchesCategoryFilter(item, filterKey) {
  if (!filterKey || filterKey === "all") return true;
  const cat = (item.category || "").toLowerCase();
  if (filterKey === "sistema") {
    return (
      cat.includes("sysmodule") ||
      cat.includes("mandos") ||
      cat.includes("overlay") ||
      cat.includes("utilidades") ||
      cat.includes("overclock") ||
      cat.includes("pantalla") ||
      cat.includes("streaming")
    );
  }
  if (filterKey === "instalador") {
    return (
      cat.includes("instalador") ||
      cat.includes("menú") ||
      cat.includes("gestor") ||
      cat.includes("emulación")
    );
  }
  if (filterKey === "red") {
    return cat.includes("online") || cat.includes("red") || cat.includes("seguridad");
  }
  if (filterKey === "partidas") {
    return cat.includes("partidas") || cat.includes("cuentas");
  }
  return true;
}

function applyStaticTranslations() {
  const tr = t();
  document.documentElement.lang = state.lang;

  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.lang === state.lang);
  });

  document.getElementById("txtHeroTagline").textContent = tr.heroTagline;
  document.getElementById("lblPillFw").textContent = tr.pillFw;
  document.getElementById("pillFwBox").title = tr.pillFwTitle;
  document.getElementById("pillAtmoBox").title = tr.pillAtmoTitle;
  document.getElementById("pillHekateBox").title = tr.pillHekateTitle;
  document.getElementById("txtBtnGlossary").textContent = tr.btnGlossary;

  document.getElementById("txtPresetsLabel").textContent = tr.presetsLabel;
  document.getElementById("txtPresetRec").textContent = tr.presetRec;
  document.getElementById("presetRecommended").title = tr.presetRecTitle;
  document.getElementById("txtPresetMin").textContent = tr.presetMin;
  document.getElementById("presetMinimal").title = tr.presetMinTitle;
  document.getElementById("txtPresetFull").textContent = tr.presetFull;
  document.getElementById("presetFull").title = tr.presetFullTitle;

  document.getElementById("txtStep1Title").textContent = tr.step1Title;
  document.getElementById("txtCompatBadge").textContent = tr.compatBadge;
  document.getElementById("txtIncompatTitle").textContent = tr.incompatTitle;
  document.getElementById("txtLabelFwSelect").textContent = tr.labelFwSelect;
  document.getElementById("tipFwSelect").title = tr.tipFwSelect;
  document.getElementById("txtFwHelp").textContent = tr.fwHelp;
  document.getElementById("txtChkIncludeFw").innerHTML = tr.chkIncludeFwHtml;
  document.getElementById("lblChkIncludeFw").title = tr.chkIncludeFwTitle;
  document.getElementById("txtLabelBaseSelect").textContent = tr.labelBaseSelect;
  document.getElementById("tipBaseSelect").title = tr.tipBaseSelect;

  document.getElementById("txtStep2Title").textContent = tr.step2Title;
  document.getElementById("txtGridExplainer").innerHTML = tr.gridExplainerHtml;
  document.getElementById("inputSearchApps").placeholder = tr.searchPlaceholder;
  document.getElementById("catAll").textContent = tr.catAll;
  document.getElementById("catSys").textContent = tr.catSys;
  document.getElementById("catInst").textContent = tr.catInst;
  document.getElementById("catNet").textContent = tr.catNet;
  document.getElementById("catSave").textContent = tr.catSave;

  document.getElementById("txtStep3Title").textContent = tr.step3Title;
  document.getElementById("tipPayloads").title = tr.tipPayloads;
  document.getElementById("txtStep3Sub").innerHTML = tr.step3SubHtml;

  document.getElementById("txtUsbPanelTitle").textContent = tr.usbPanelTitle;
  document.getElementById("txtHekateGuideTitle").textContent = tr.hekateGuideTitle;
  document.getElementById("listHekateSteps").innerHTML = `
    <li>${tr.hekateStep1Html}</li>
    <li>${tr.hekateStep2Html}</li>
    <li>${tr.hekateStep3Html}</li>
  `;
  document.getElementById("txtSdDriveLabel").textContent = tr.sdDriveLabel;
  document.getElementById("txtBtnRefreshSd").textContent = tr.btnRefreshSd;
  document.getElementById("txtBtnExploreSd").textContent = tr.btnExploreSd;
  document.getElementById("txtBtnEjectSd").textContent = tr.btnEjectSd;

  document.getElementById("lblSumBase").textContent = tr.lblSumBase;
  document.getElementById("lblSumFw").textContent = tr.lblSumFw;
  document.getElementById("lblSumApps").textContent = tr.lblSumApps;
  document.getElementById("lblSumTotal").textContent = tr.lblSumTotal;
  document.getElementById("lblSumCached").textContent = tr.lblSumCached;
  document.getElementById("lblSumDownload").textContent = tr.lblSumDownload;
  document.getElementById("txtTreeTitle").textContent = tr.treeTitle;
  document.getElementById("btnClearCache").textContent = tr.btnClearCache;
  document.getElementById("txtBtnBuild").textContent = tr.btnBuild;

  if (!state.pollTimer) {
    document.getElementById("progressStatusText").textContent = tr.statusWaiting;
  }

  // Modal Confirmación
  document.getElementById("txtConfirmModalTitle").textContent = tr.confirmModalTitle;
  document.getElementById("txtConfirmDetail").innerHTML = tr.confirmDetailHtml;
  document.getElementById("txtPillEmummc").textContent = tr.pillEmummc;
  document.getElementById("txtPillNintendo").textContent = tr.pillNintendo;
  document.getElementById("txtConfirmNote").textContent = tr.confirmNote;
  document.getElementById("btnCancelConfirmModal").textContent = tr.btnCancel;
  document.getElementById("btnAcceptConfirmModal").textContent = tr.btnAcceptConfirm;

  // Modal Glosario
  document.getElementById("txtGlossaryModalTitle").textContent = tr.glossaryModalTitle;
  document.getElementById("btnOkGlossaryModal").textContent = tr.btnOkGlossary;
  const gBody = document.getElementById("glossaryModalBody");
  gBody.innerHTML = "";
  tr.glossaryItems.forEach((g) => {
    const itemDiv = document.createElement("div");
    itemDiv.className = "glossary-item";
    const strong = document.createElement("strong");
    strong.textContent = g.title;
    const p = document.createElement("p");
    p.textContent = g.desc;
    itemDiv.appendChild(strong);
    itemDiv.appendChild(p);
    gBody.appendChild(itemDiv);
  });

  if (state.catalogData) {
    document.getElementById("cacheInfoText").textContent = tr.cacheInfo(
      state.catalogData.cache_size_mb,
      state.catalogData.cache_count
    );
    updateGhSyncIndicator(state.catalogData.gh_sync);
    renderHeaderAndSelectors(state.catalogData);
    renderSdDrives(state.sdDrives);
    renderAllGrids();
    renderSummary(state.catalogData);
  }
}

async function fetchState(preserveSelection = true) {
  const qs = new URLSearchParams({
    fw: state.userChangedFw ? state.targetFirmware : "",
    base: state.userChangedBase ? state.basePackTag : "",
  });
  const res = await fetch(`/api/state?${qs.toString()}`);
  const data = await res.json();
  state.catalogData = data;
  state.sdDrives = data.sd_drives || [];
  state.targetFirmware = data.target_firmware;
  if (!state.userChangedBase || state.basePackTag !== "auto") {
    state.basePackTag = data.base_pack ? data.base_pack.tag : "";
  }

  document.getElementById("cacheInfoText").textContent = t().cacheInfo(
    data.cache_size_mb,
    data.cache_count
  );

  updateGhSyncIndicator(data.gh_sync);

  if (!state.initializedDefaults || !preserveSelection) {
    applyPresetSelection("recommended", data, false);
    state.initializedDefaults = true;
  }

  renderHeaderAndSelectors(data);
  renderSdDrives(state.sdDrives);
  renderAllGrids();
  renderSummary(data);

  if (data.gh_sync && data.gh_sync.checking) {
    setTimeout(waitForStartupGhSync, 600);
  } else if (data.gh_sync && data.gh_sync.checked) {
    state.ghSyncApplied = true;
  }
}

async function waitForStartupGhSync() {
  if (state.ghSyncApplied) return;
  try {
    const res = await fetch("/api/state?fw=&base=");
    const data = await res.json();
    if (data.gh_sync && data.gh_sync.checking) {
      setTimeout(waitForStartupGhSync, 600);
      return;
    }
    state.ghSyncApplied = true;
    state.customVersions = {};
    await fetchState(true);
  } catch (_) {}
}

function updateGhSyncIndicator(ghSync) {
  const dot = document.getElementById("syncNotifDot");
  const btn = document.getElementById("btnSyncGh");
  const lbl = document.getElementById("syncBtnLabel");
  const tr = t();
  dot.classList.add("hidden");
  if (!ghSync) return;

  if (ghSync.checking) {
    lbl.textContent = tr.syncChecking;
  } else {
    lbl.textContent = tr.syncNormal;
    btn.title =
      ghSync.checked && ghSync.count > 0
        ? tr.syncTooltipUpdates(ghSync.updated)
        : tr.syncTooltipOk;
  }
}

function applyPresetSelection(presetName, data = state.catalogData, rerender = true) {
  if (!data) return;
  state.activePreset = presetName;
  state.selectedApps.clear();
  state.selectedPayloads.clear();

  if (presetName === "recommended") {
    data.apps.forEach((a) => {
      if (a.default_selected) state.selectedApps.add(a.id);
    });
    data.payloads.forEach((p) => {
      if (p.default_selected) state.selectedPayloads.add(p.id);
    });
  } else if (presetName === "minimal") {
    data.apps.forEach((a) => {
      if (a.id === "quick_reboot") state.selectedApps.add(a.id);
    });
  } else if (presetName === "full") {
    data.apps.forEach((a) => state.selectedApps.add(a.id));
    data.payloads.forEach((p) => state.selectedPayloads.add(p.id));
  }

  updatePresetButtonsUI();
  if (rerender) {
    renderAllGrids();
    renderSummary(data);
  }
}

function updatePresetButtonsUI() {
  document.querySelectorAll(".preset-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.preset === state.activePreset);
  });
}

async function refreshDrivesOnly() {
  if (state.pollTimer) return;
  try {
    const fwParam = state.userChangedFw ? state.targetFirmware : "";
    const baseParam = state.userChangedBase ? state.basePackTag : "";
    const res = await fetch(
      `/api/state?fw=${encodeURIComponent(fwParam)}&base=${encodeURIComponent(baseParam)}`
    );
    const data = await res.json();
    state.sdDrives = data.sd_drives || [];
    renderSdDrives(state.sdDrives);
    updateGhSyncIndicator(data.gh_sync);
    if (!state.ghSyncApplied && data.gh_sync && data.gh_sync.checked) {
      state.ghSyncApplied = true;
      state.customVersions = {};
      await fetchState(true);
    }
  } catch (_) {}
}

function renderSdDrives(drives) {
  const select = document.getElementById("selectSdDrive");
  const statusEl = document.getElementById("sdDriveStatusBadge");
  const tr = t();
  select.innerHTML = "";

  if (!drives || drives.length === 0) {
    state.selectedDrive = "";
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = tr.noSdDetectedOpt;
    select.appendChild(opt);
    statusEl.className = "sd-status-info disconnected";
    statusEl.innerHTML = tr.noSdStatusHtml;
    return;
  }

  const stillExists = drives.some((d) => d.drive === state.selectedDrive);
  if (!stillExists) {
    state.selectedDrive = drives[0].drive;
  }

  drives.forEach((d) => {
    const opt = document.createElement("option");
    opt.value = d.drive;
    const switchTag = d.is_switch_sd ? "🎮 [Switch SD]" : "💾 [USB/SD]";
    opt.textContent = `${d.drive} (${d.label}) ${switchTag} — ${tr.sdFreeOfTotal(d.free_gb, d.total_gb)} [${d.fs_type}]`;
    if (d.drive === state.selectedDrive) opt.selected = true;
    select.appendChild(opt);
  });

  const activeDriveObj = drives.find((d) => d.drive === state.selectedDrive) || drives[0];
  statusEl.className = "sd-status-info connected";
  const badgesText =
    activeDriveObj.detected_badges && activeDriveObj.detected_badges.length > 0
      ? tr.sdDetectedBadges(escapeHtml(activeDriveObj.detected_badges.join(", ")))
      : tr.sdReadyClean;
  statusEl.innerHTML = `✅ ${tr.sdConnectedIn} <strong>${escapeHtml(activeDriveObj.drive)}</strong> (${escapeHtml(activeDriveObj.fs_type)}) | ${badgesText}`;
}

function renderHeaderAndSelectors(data) {
  const base = data.base_pack;
  const tr = t();
  document.getElementById("badgeFw").textContent = data.target_firmware;
  document.getElementById("badgeAtmo").textContent = `v${base.atmosphere || "1.12.1"}`;
  document.getElementById("badgeHekate").textContent = `v${base.hekate || "6.5.4"}`;

  const incompatBanner = document.getElementById("fwIncompatibilityBanner");
  const incompatText = document.getElementById("fwIncompatibilityText");
  if (data.fw_incompatible) {
    incompatText.textContent = tr.incompatMsg(
      base.tag,
      base.atmosphere,
      base.max_fw,
      data.target_firmware
    );
    incompatBanner.classList.remove("hidden");
  } else {
    incompatBanner.classList.add("hidden");
  }

  const fwSelect = document.getElementById("selectFirmware");
  fwSelect.innerHTML = "";
  data.all_firmwares.forEach((fw, idx) => {
    const opt = document.createElement("option");
    opt.value = fw.version;
    const isLatest = idx === 0 ? tr.latestDefaultSuffix : "";
    opt.textContent = `Firmware ${fw.version}${isLatest} — ${formatMB(fw.size_bytes)}`;
    if (fw.version === data.target_firmware) opt.selected = true;
    fwSelect.appendChild(opt);
  });

  const baseSelect = document.getElementById("selectBasePack");
  baseSelect.innerHTML = "";
  if (
    (!state.basePackTag || state.basePackTag === "auto") &&
    data.all_base_packs &&
    data.all_base_packs.length > 0
  ) {
    state.basePackTag = data.all_base_packs[0].tag;
  }

  data.all_base_packs.forEach((b, idx) => {
    const opt = document.createElement("option");
    opt.value = b.tag;
    const isLatest = idx === 0 ? tr.latestDefaultSuffix : "";
    opt.textContent = `${b.name}${isLatest} — ${formatMB(b.size_bytes)}`;
    if (state.basePackTag === b.tag) opt.selected = true;
    baseSelect.appendChild(opt);
  });

  const autoOpt = document.createElement("option");
  autoOpt.value = "auto";
  autoOpt.textContent = tr.autoBaseOption;
  if (state.basePackTag === "auto") autoOpt.selected = true;
  baseSelect.appendChild(autoOpt);

  const infoBox = document.getElementById("basePackInfoBox");
  const cachePill = base.is_cached ? ` | ${tr.cachedBadge}` : "";
  infoBox.innerHTML = `
    <strong>${tr.baseSelectedLabel}</strong> ${escapeHtml(base.name)}<br/>
    <span>${tr.baseSupportsUpTo} <strong>${escapeHtml(base.max_fw)}</strong> | ${tr.baseSizeLabel} ${formatMB(base.size_bytes)}${cachePill}</span>
  `;
}

function renderAllGrids() {
  if (!state.catalogData) return;
  const query = state.searchQuery.trim().toLowerCase();
  const filteredApps = state.catalogData.apps.filter((app) => {
    const nameStr = getItemName(app).toLowerCase();
    const descStr = getItemDesc(app).toLowerCase();
    const catStr = getItemCategory(app).toLowerCase();
    const matchesSearch =
      !query || nameStr.includes(query) || descStr.includes(query) || catStr.includes(query);
    return matchesSearch && matchesCategoryFilter(app, state.categoryFilter);
  });

  renderCardsGrid("appsGrid", filteredApps, state.selectedApps);
  renderCardsGrid("payloadsGrid", state.catalogData.payloads, state.selectedPayloads);
}

function getActiveReleaseForItem(item) {
  const resolvedRel =
    item.resolved_release || (item.compatibility_matrix && item.compatibility_matrix[0]);
  if (state.customVersions[item.id] && item.compatibility_matrix) {
    const found = item.compatibility_matrix.find((m) => m.tag === state.customVersions[item.id]);
    if (found) return found;
  }
  return resolvedRel;
}

function renderCardsGrid(containerId, items, selectedSet) {
  const grid = document.getElementById(containerId);
  const tr = t();
  grid.innerHTML = "";

  if (items.length === 0) {
    const emptyMsg = document.createElement("div");
    emptyMsg.style.color = "var(--text-secondary)";
    emptyMsg.style.fontSize = "13px";
    emptyMsg.style.padding = "10px 4px";
    emptyMsg.textContent = tr.emptySearch;
    grid.appendChild(emptyMsg);
    return;
  }

  items.forEach((item) => {
    const isSelected = selectedSet.has(item.id);
    const keepInBase = Boolean(item.keep_base_when_unselected);
    const activeRelObj = getActiveReleaseForItem(item);
    const activeTag = activeRelObj ? activeRelObj.tag : "N/A";

    const card = document.createElement("div");
    card.className = `item-card ${isSelected ? "selected" : ""}`;

    let badgeClass = "skip-app";
    let badgeText = tr.badgeSkip;
    let badgeTitle = tr.badgeSkipTitle;

    if (isSelected) {
      badgeClass = "installed-app";
      badgeText = tr.badgeInstall;
      badgeTitle = tr.badgeInstallTitle;
    } else if (keepInBase) {
      badgeClass = "base-included";
      badgeText = getItemBaseBadge(item);
      badgeTitle = tr.badgeBaseTitle;
    }

    const topWrapper = document.createElement("div");

    const cardTop = document.createElement("div");
    cardTop.className = "card-top";

    const titleGroup = document.createElement("div");
    titleGroup.className = "card-title-group";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = isSelected;
    checkbox.dataset.id = item.id;

    const titleTexts = document.createElement("div");
    const nameEl = document.createElement("div");
    nameEl.className = "card-name";
    nameEl.textContent = getItemName(item);

    const catEl = document.createElement("div");
    catEl.className = "card-category";
    catEl.textContent = getItemCategory(item);

    titleTexts.appendChild(nameEl);
    titleTexts.appendChild(catEl);
    titleGroup.appendChild(checkbox);
    titleGroup.appendChild(titleTexts);

    const badgeGroup = document.createElement("div");
    badgeGroup.className = "badge-group";
    const statusBadge = document.createElement("span");
    statusBadge.className = `status-badge ${badgeClass}`;
    statusBadge.title = badgeTitle;
    statusBadge.textContent = badgeText;
    badgeGroup.appendChild(statusBadge);

    cardTop.appendChild(titleGroup);
    cardTop.appendChild(badgeGroup);

    const descEl = document.createElement("p");
    descEl.className = "card-desc";
    descEl.style.marginTop = "8px";
    descEl.textContent = getItemDesc(item);

    topWrapper.appendChild(cardTop);
    topWrapper.appendChild(descEl);

    const footer = document.createElement("div");
    footer.className = "card-footer";

    const verLabel = document.createElement("span");
    verLabel.style.color = "var(--text-secondary)";
    verLabel.textContent = `${tr.versionPrefix} ${activeTag}`;
    footer.appendChild(verLabel);

    const sizeAndCache = document.createElement("span");
    const isCached = activeRelObj && activeRelObj.is_cached;
    sizeAndCache.textContent = activeRelObj
      ? `${formatMB(activeRelObj.size_bytes)}${isCached ? " ⚡" : ""}`
      : "";
    if (isCached) {
      sizeAndCache.title = tr.cachedTitle;
      sizeAndCache.style.color = "var(--accent-green)";
    }
    footer.appendChild(sizeAndCache);

    card.appendChild(topWrapper);
    card.appendChild(footer);

    card.addEventListener("click", () => {
      if (selectedSet.has(item.id)) {
        selectedSet.delete(item.id);
      } else {
        selectedSet.add(item.id);
      }
      state.activePreset = "custom";
      updatePresetButtonsUI();
      renderAllGrids();
      renderSummary(state.catalogData);
    });

    grid.appendChild(card);
  });
}

function renderSummary(data) {
  if (!data) return;
  const base = data.base_pack;
  const fw = data.firmware_release;
  const tr = t();

  document.getElementById("sumBasePack").textContent = `${base.tag} (Atmo ${base.atmosphere})`;

  if (state.includeFirmwareFiles && fw) {
    document.getElementById("sumFirmware").textContent = `${fw.version} (${formatMB(fw.size_bytes)})`;
  } else {
    document.getElementById("sumFirmware").textContent = tr.noFwFolder(data.target_firmware);
  }

  document.getElementById("sumAppsCount").textContent =
    `${state.selectedApps.size} apps / ${state.selectedPayloads.size} payloads`;

  let totalInstallBytes = 0;
  let cachedBytes = 0;

  const accountBytes = (size, isCached) => {
    const sz = size || 0;
    totalInstallBytes += sz;
    if (isCached) cachedBytes += sz;
  };

  accountBytes(base.size_bytes, base.is_cached);
  if (state.includeFirmwareFiles && fw) {
    accountBytes(fw.size_bytes, fw.is_cached);
  }

  const changesList = document.getElementById("changesPreviewList");
  changesList.innerHTML = "";

  const addChange = (cls, text) => {
    const li = document.createElement("li");
    li.className = cls;
    li.textContent = text;
    changesList.appendChild(li);
  };

  addChange("remove", tr.treeKeepProtected);
  addChange("update", tr.treeBasePack(base.tag));
  if (state.includeFirmwareFiles && fw) {
    addChange("add", tr.treeFwDaybreak(fw.version));
  }

  data.apps.forEach((app) => {
    const isSel = state.selectedApps.has(app.id);
    const activeRel = getActiveReleaseForItem(app);
    const tag = activeRel ? activeRel.tag : "";
    if (isSel) {
      if (activeRel) accountBytes(activeRel.size_bytes, activeRel.is_cached);
      addChange("add", `✓ ${getItemName(app)} (${tag})`);
    } else if (app.keep_base_when_unselected) {
      addChange("update", `✓ ${getItemBaseBadge(app)} ${tr.treeInBaseSuffix}`);
    }
  });

  data.payloads.forEach((pl) => {
    const isSel = state.selectedPayloads.has(pl.id);
    const activeRel = getActiveReleaseForItem(pl);
    const tag = activeRel ? activeRel.tag : "";
    if (isSel) {
      if (activeRel) accountBytes(activeRel.size_bytes, activeRel.is_cached);
      addChange("add", `✓ Payload: ${getItemName(pl)} (${tag})`);
    } else if (pl.keep_base_when_unselected) {
      addChange("update", `✓ Payload: ${getItemName(pl)} ${tr.treeInBaseSuffix}`);
    }
  });

  const toDownloadBytes = Math.max(0, totalInstallBytes - cachedBytes);
  document.getElementById("sumTotalInstallSize").textContent = `~${formatMB(totalInstallBytes)}`;
  document.getElementById("sumCachedSize").textContent = formatMB(cachedBytes);
  document.getElementById("sumToDownloadSize").textContent =
    toDownloadBytes === 0 ? tr.allInCache : `~${formatMB(toDownloadBytes)}`;
}

function openCleanInstallWarningModal() {
  const tr = t();
  if (!state.selectedDrive) {
    alert(tr.alertNoSd);
    return;
  }

  if (state.catalogData && state.catalogData.fw_incompatible) {
    const base = state.catalogData.base_pack;
    const msg = tr.incompatMsg(
      base.tag,
      base.atmosphere,
      base.max_fw,
      state.catalogData.target_firmware
    );
    if (!confirm(tr.alertIncompatConfirm(msg))) return;
  }

  const driveObj = state.sdDrives.find((d) => d.drive === state.selectedDrive);
  const labelText = driveObj
    ? `${driveObj.drive} (${driveObj.label} — ${driveObj.total_gb} GB)`
    : state.selectedDrive;

  document.getElementById("txtConfirmLead").innerHTML = tr.confirmLeadHtml(escapeHtml(labelText));
  document.getElementById("confirmInstallModalBackdrop").classList.remove("hidden");
}

async function executeBuildPackAfterConfirm() {
  document.getElementById("confirmInstallModalBackdrop").classList.add("hidden");
  const btn = document.getElementById("btnBuildPack");
  btn.disabled = true;

  const payload = {
    target_drive: state.selectedDrive,
    target_firmware: state.targetFirmware,
    include_firmware_files: state.includeFirmwareFiles,
    base_pack_tag: state.basePackTag,
    selected_apps: Array.from(state.selectedApps),
    selected_payloads: Array.from(state.selectedPayloads),
    custom_versions: state.customVersions,
  };

  try {
    const res = await fetch("/api/build", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!data.ok) {
      alert(data.error || "Error");
      btn.disabled = false;
      return;
    }
    startPollingStatus();
  } catch (err) {
    alert("Error: " + err);
    btn.disabled = false;
  }
}

function startPollingStatus() {
  if (state.pollTimer) clearInterval(state.pollTimer);
  state.pollTimer = setInterval(async () => {
    try {
      const res = await fetch("/api/build/status");
      const st = await res.json();

      document.getElementById("progressStatusText").textContent = st.message || "";
      document.getElementById("progressPercentText").textContent = `${st.progress || 0}%`;
      document.getElementById("progressBarFill").style.width = `${st.progress || 0}%`;

      const logsBox = document.getElementById("consoleLogs");
      logsBox.innerHTML = "";
      (st.logs || []).forEach((line) => {
        const div = document.createElement("div");
        div.textContent = line;
        logsBox.appendChild(div);
      });
      logsBox.scrollTop = logsBox.scrollHeight;

      if (!st.running) {
        clearInterval(state.pollTimer);
        state.pollTimer = null;
        document.getElementById("btnBuildPack").disabled = false;
        fetchState(true);
      }
    } catch (e) {
      console.error(e);
    }
  }, 500);
}

// Bloquear menú contextual e inspector en el .exe
document.addEventListener("contextmenu", (e) => e.preventDefault());
document.addEventListener("keydown", (e) => {
  if (
    e.key === "F12" ||
    (e.ctrlKey && e.shiftKey && (e.key === "I" || e.key === "J" || e.key === "C")) ||
    (e.ctrlKey && e.key === "u")
  ) {
    e.preventDefault();
  }
});

// EVENT LISTENERS
document.addEventListener("DOMContentLoaded", () => {
  applyStaticTranslations();
  fetchState(false);

  state.driveAutoTimer = setInterval(refreshDrivesOnly, 4000);

  // Selector de idioma (ES / EN)
  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.lang = btn.dataset.lang;
      applyStaticTranslations();
    });
  });

  // Presets ("Recomendado", "Mínimo", "Completo")
  document.querySelectorAll(".preset-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      applyPresetSelection(btn.dataset.preset);
    });
  });

  // Buscador de aplicaciones
  document.getElementById("inputSearchApps").addEventListener("input", (e) => {
    state.searchQuery = e.target.value;
    renderAllGrids();
  });

  // Píldoras de filtro por categoría
  document.querySelectorAll(".cat-pill").forEach((pill) => {
    pill.addEventListener("click", () => {
      state.categoryFilter = pill.dataset.cat;
      document.querySelectorAll(".cat-pill").forEach((p) => {
        p.classList.toggle("active", p.dataset.cat === state.categoryFilter);
      });
      renderAllGrids();
    });
  });

  // Modal Glosario
  const glossaryModal = document.getElementById("glossaryModalBackdrop");
  document.getElementById("btnOpenGlossary").addEventListener("click", () =>
    glossaryModal.classList.remove("hidden")
  );
  document.getElementById("btnCloseGlossaryModal").addEventListener("click", () =>
    glossaryModal.classList.add("hidden")
  );
  document.getElementById("btnOkGlossaryModal").addEventListener("click", () =>
    glossaryModal.classList.add("hidden")
  );

  document.getElementById("selectSdDrive").addEventListener("change", (e) => {
    state.selectedDrive = e.target.value;
    renderSdDrives(state.sdDrives);
  });

  document.getElementById("btnRefreshDrives").addEventListener("click", refreshDrivesOnly);

  document.getElementById("btnOpenDrive").addEventListener("click", async () => {
    if (!state.selectedDrive) {
      alert(t().alertNoSd);
      return;
    }
    await fetch("/api/open-drive", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ drive: state.selectedDrive }),
    });
  });

  document.getElementById("btnEjectDrive").addEventListener("click", async () => {
    if (!state.selectedDrive) {
      alert(t().alertNoSd);
      return;
    }
    const btn = document.getElementById("btnEjectDrive");
    const spanTxt = document.getElementById("txtBtnEjectSd");
    btn.disabled = true;
    spanTxt.textContent = t().ejectingText;
    try {
      const res = await fetch("/api/eject-drive", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ drive: state.selectedDrive }),
      });
      const data = await res.json();
      await refreshDrivesOnly();
      if (data.ok) {
        const statusEl = document.getElementById("sdDriveStatusBadge");
        statusEl.className = "sd-status-info connected";
        statusEl.textContent = `⏏️ ${data.message}`;
      } else {
        alert(data.message || "Error");
      }
    } catch (e) {
      alert("Error: " + e);
    } finally {
      btn.disabled = false;
      spanTxt.textContent = t().btnEjectSd;
    }
  });

  document.getElementById("selectFirmware").addEventListener("change", (e) => {
    state.targetFirmware = e.target.value;
    state.userChangedFw = true;
    state.customVersions = {};
    fetchState(true);
  });

  document.getElementById("selectBasePack").addEventListener("change", (e) => {
    state.basePackTag = e.target.value;
    state.userChangedBase = true;
    state.customVersions = {};
    fetchState(true);
  });

  document.getElementById("chkIncludeFwFiles").addEventListener("change", (e) => {
    state.includeFirmwareFiles = e.target.checked;
    renderSummary(state.catalogData);
  });

  document.getElementById("btnBuildPack").addEventListener("click", openCleanInstallWarningModal);

  const confirmModal = document.getElementById("confirmInstallModalBackdrop");
  document.getElementById("btnCloseConfirmModal").addEventListener("click", () =>
    confirmModal.classList.add("hidden")
  );
  document.getElementById("btnCancelConfirmModal").addEventListener("click", () =>
    confirmModal.classList.add("hidden")
  );
  document.getElementById("btnAcceptConfirmModal").addEventListener("click", executeBuildPackAfterConfirm);

  document.getElementById("btnSyncGh").addEventListener("click", async () => {
    const btn = document.getElementById("btnSyncGh");
    const lbl = document.getElementById("syncBtnLabel");
    btn.disabled = true;
    lbl.textContent = t().syncChecking;
    try {
      const res = await fetch("/api/sync", { method: "POST", body: "{}" });
      const data = await res.json();
      state.userChangedFw = false;
      state.userChangedBase = false;
      state.customVersions = {};
      await fetchState(true);
      if (data.count > 0) {
        alert(t().syncTooltipUpdates(data.updated));
      } else {
        alert(t().syncTooltipOk);
      }
    } catch (e) {
      alert("Error: " + e);
    } finally {
      btn.disabled = false;
    }
  });

  document.getElementById("btnClearCache").addEventListener("click", async () => {
    await fetch("/api/clear-cache", { method: "POST", body: "{}" });
    fetchState(true);
  });
});
