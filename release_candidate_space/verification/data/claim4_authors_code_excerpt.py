# Authors' repository revision:
# 6633b553a244634bd2c2e1142603aad1c1fbe55a
# train.py, relevant MMD-GAN training fragment
#
# for each inner iteration:
#     # (1) Optimise discriminator
#     for p in netD.parameters():
#         p.requires_grad = True
#     if args.kernel == "learned_kernel":
#         for p in kernel.parameters():
#             p.requires_grad = True
#     for _ in range(args.D_steps):
#         d_loss = compute_D_loss(args, z, real_images, d_real, d_fake, kernel)
#         optimizerD.zero_grad(set_to_none=True)
#         d_loss.backward()
#         optimizerD.step()
#
# The authors' documented Equation-18 configuration is:
# python train.py --dataset cifar10 --divergence MMD --JKO ...
# The default kernel is learned_kernel and D_steps defaults to 1.
