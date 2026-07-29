# Claim 4 source audit

Section 4 distinguishes fixed-kernel Algorithm 1, whose witness is available in
closed form, from adaptive-kernel Equation (18):

`max_phi min_T 1/2 ||Id-T||² + MMD²_{k_phi}(T#mu_l,nu)`.

The paper explicitly calls Equation (18) adversarial. Appendix D.4 gives
`phi* in argmax_phi 1/2 MMD²_{k_phi}` and Algorithm 2 updates `phi`. At authors'
code revision `6633b553a244634bd2c2e1142603aad1c1fbe55a`, the documented
MMD+JKO path executes `optimizerD.step()`.

Paper HTML SHA-256:
`9e465ccada2014404d315c46108399b4ee49693d09d9866ff3dbd426045fd30a`.
