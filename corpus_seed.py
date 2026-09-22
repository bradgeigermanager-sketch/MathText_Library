"""
FORM ID: MATHTEXT_CORPUS_SEED_V1
PURPOSE: Pre-packaged mathematical documents for indexing, search benchmarking, and export.
"""

from typing import Dict

CORPUS: Dict[str, Dict[str, str]] = {
    "doc_diffgeom": {
        "title": "Differential Geometry & Curvature Forms",
        "category": "Topology / Geometry",
        "content": (
            "## Differential Geometry & Curvature Forms\n\n"
            "Let $(M, g)$ be an $n$-dimensional smooth Riemannian manifold equipped with the Levi-Civita connection $\\nabla$.\n\n"
            "The Riemann curvature tensor field $R$ of type $(1, 3)$ is defined by:\n"
            "$$R(X, Y)Z = \\nabla_X \\nabla_Y Z - \\nabla_Y \\nabla_X Z - \\nabla_{[X, Y]} Z$$\n\n"
            "In local coordinates $(x^1, \\dots, x^n)$, the components $R^l_{ijk}$ satisfy:\n"
            "$$R^l_{ijk} = \\partial_j \\Gamma^l_{ik} - \\partial_k \\Gamma^l_{ij} + \\Gamma^m_{ik}\\Gamma^l_{mj} - \\Gamma^m_{ij}\\Gamma^l_{mk}$$\n\n"
            "The Ricci curvature tensor is obtained through index contraction:\n"
            "$$R_{ij} = R^k_{ikj}$$\n\n"
            "Scalar curvature $S$ represents the full contraction with the inverse metric tensor $g^{ij}$:\n"
            "$$S = g^{ij} R_{ij}$$\n\n"
            "For a compact 2-manifold $M$ without boundary, the Gauss-Bonnet theorem guarantees:\n"
            "$$\\int_M K \\, dA = 2\\pi \\chi(M)$$\n"
            "where $K$ is the Gaussian curvature and $\\chi(M)$ denotes the Euler characteristic."
        ),
    },
    "doc_electrodynamics": {
        "title": "Covariant Classical Electrodynamics",
        "category": "Field Theory",
        "content": (
            "## Covariant Classical Electrodynamics\n\n"
            "In Minkowski spacetime with signature $(-, +, +, +)$, Maxwell's equations can be written in manifest 4-vector form.\n\n"
            "The electromagnetic field strength tensor $F^{\\mu\\nu}$ is given in terms of the four-potential $A^\\mu = (\\phi/c, \\mathbf{A})$ as:\n"
            "$$F^{\\mu\\nu} = \\partial^\\mu A^\\nu - \\partial^\\nu A^\\mu$$\n\n"
            "The inhomogeneous Maxwell equations with four-current density $J^\\mu = (c\\rho, \\mathbf{J})$ are expressed as:\n"
            "$$\\partial_\\mu F^{\\mu\\nu} = \\mu_0 J^\\nu$$\n\n"
            "The homogeneous equations reduce to the Bianchi identity:\n"
            "$$\\partial_\\lambda F_{\\mu\\nu} + \\partial_\\mu F_{\\nu\\lambda} + \\partial_\\nu F_{\\lambda\\mu} = 0$$\n\n"
            "The symmetric stress-energy-momentum tensor of the electromagnetic field takes the form:\n"
            "$$T^{\\mu\\nu} = \\frac{1}{\\mu_0} \\left( F^{\\mu\\alpha} F^\\nu{}_\\alpha - \\frac{1}{4}\\eta^{\\mu\\nu} F_{\\alpha\\beta}F^{\\alpha\\beta} \\right)$$\n\n"
            "Conservation of energy and linear momentum follows directly:\n"
            "$$\\partial_\\mu T^{\\mu\\nu} = -F^{\\nu\\lambda} J_\\lambda$$"
        ),
    },
    "doc_fourier_analysis": {
        "title": "Harmonic Analysis & Fourier Transforms",
        "category": "Analysis / Signal Processing",
        "content": (
            "## Harmonic Analysis & Fourier Transforms\n\n"
            "Let $f \\in L^1(\\mathbb{R}^n) \\cap L^2(\\mathbb{R}^n)$. The continuous Fourier transform $\\mathcal{F}\\{f\\} = \\hat{f}$ is defined by:\n"
            "$$\\hat{f}(\\xi) = \\int_{\\mathbb{R}^n} f(x) e^{-2\\pi i \\langle x, \\xi \\rangle} \\, dx$$\n\n"
            "The inverse transform recovers $f(x)$ almost everywhere:\n"
            "$$f(x) = \\int_{\\mathbb{R}^n} \\hat{f}(\\xi) e^{2\\pi i \\langle x, \\xi \\rangle} \\, d\\xi$$\n\n"
            "By the Plancherel theorem, the transform is an isometry on $L^2(\\mathbb{R}^n)$:\n"
            "$$\\|f\\|_{L^2}^2 = \\int_{\\mathbb{R}^n} |f(x)|^2 \\, dx = \\int_{\\mathbb{R}^n} |\\hat{f}(\\xi)|^2 \\, d\\xi = \\|\\hat{f}\\|_{L^2}^2$$\n\n"
            "Under convolution $(f * g)(x) = \\int_{\\mathbb{R}^n} f(y)g(x - y)\\,dy$, the operator diagonalizes:\n"
            "$$\\mathcal{F}\\{f * g\\} = \\hat{f}(\\xi) \\cdot \\hat{g}(\\xi)$$\n\n"
            "The Heisenberg-Pauli-Weyl uncertainty principle sets the bound:\n"
            "$$\\left( \\int_{-\\infty}^\\infty x^2 |f(x)|^2 \\, dx \\right) \\left( \\int_{-\\infty}^\\infty \\xi^2 |\\hat{f}(\\xi)|^2 \\, d\\xi \\right) \\ge \\frac{\\|f\\|_{L^2}^4}{16\\pi^2}$$"
        ),
    },
    "doc_quantum_info": {
        "title": "Quantum Density Operators & Von Neumann Entropy",
        "category": "Quantum Information",
        "content": (
            "## Quantum Density Operators & Von Neumann Entropy\n\n"
            "A mixed quantum state on Hilbert space $\\mathcal{H}$ is characterized by a density operator $\\rho$ satisfying:\n"
            "$$\\rho = \\sum_i p_i |\\psi_i\\rangle\\langle\\psi_i|, \\quad p_i \\ge 0, \\quad \\sum_i p_i = 1$$\n\n"
            "The operator satisfies hermiticity $\\rho = \\rho^\\dagger$, positive semidefiniteness $\\rho \\succeq 0$, and unit trace:\n"
            "$$\\operatorname{Tr}(\\rho) = 1$$\n\n"
            "The Von Neumann entropy quantifying statistical disorder or entanglement entropy is:\n"
            "$$S(\\rho) = -\\operatorname{Tr}(\\rho \\ln \\rho) = -\\sum_k \\lambda_k \\ln \\lambda_k$$\n\n"
            "For a bipartite composite system $\\mathcal{H}_A \\otimes \\mathcal{H}_B$, the partial trace determines the reduced state:\n"
            "$$\\rho_A = \\operatorname{Tr}_B(\\rho_{AB}) = \\sum_k (I_A \\otimes \\langle k_B|) \\rho_{AB} (I_A \\otimes |k_B\\rangle)$$\n\n"
            "Subadditivity of the quantum entropy holds unconditionally:\n"
            "$$S(\\rho_{AB}) \\le S(\\rho_A) + S(\\rho_B)$$"
        ),
    },
    "doc_navier_stokes": {
        "title": "Incompressible Navier-Stokes Equations",
        "category": "Continuum Mechanics",
        "content": (
            "## Incompressible Navier-Stokes Equations\n\n"
            "The governing equations for a viscous, incompressible Newtonian fluid in domain $\\Omega \\subset \\mathbb{R}^3$ are:\n"
            "$$\\frac{\\partial \\mathbf{u}}{\\partial t} + (\\mathbf{u} \\cdot \\nabla)\\mathbf{u} = -\\frac{1}{\\rho}\\nabla p + \\nu \\nabla^2 \\mathbf{u} + \\mathbf{f}$$\n\n"
            "The incompressibility constraint enforces a divergence-free velocity field:\n"
            "$$\\nabla \\cdot \\mathbf{u} = 0$$\n\n"
            "The Reynolds number $\\text{Re}$ characterizes the ratio of inertial forces to viscous forces:\n"
            "$$\\text{Re} = \\frac{u_0 L}{\\nu}$$\n\n"
            "Taking the curl of momentum yields the vorticity transport equation for $\\boldsymbol{\\omega} = \\nabla \\times \\mathbf{u}$:\n"
            "$$\\frac{\\partial \\boldsymbol{\\omega}}{\\partial t} + (\\mathbf{u} \\cdot \\nabla)\\boldsymbol{\\omega} = (\\boldsymbol{\\omega} \\cdot \\nabla)\\mathbf{u} + \\nu \\nabla^2 \\boldsymbol{\\omega}$$"
        ),
    },
}

