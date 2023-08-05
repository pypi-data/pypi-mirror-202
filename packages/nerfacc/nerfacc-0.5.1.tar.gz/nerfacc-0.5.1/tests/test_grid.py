import pytest
import torch

device = "cuda:0"


@pytest.mark.skipif(not torch.cuda.is_available, reason="No CUDA device")
def test_ray_aabb_intersect():
    from nerfacc.grid import _ray_aabb_intersect, ray_aabb_intersect

    torch.manual_seed(42)
    n_rays = 1000
    n_aabbs = 100

    rays_o = torch.rand((n_rays, 3), device=device)
    rays_d = torch.randn((n_rays, 3), device=device)
    rays_d = rays_d / rays_d.norm(dim=-1, keepdim=True)
    aabb_min = torch.rand((n_aabbs, 3), device=device)
    aabb_max = aabb_min + torch.rand_like(aabb_min)
    aabbs = torch.cat([aabb_min, aabb_max], dim=-1)

    # [n_rays, n_aabbs]
    tmins, tmaxs, hits = ray_aabb_intersect(rays_o, rays_d, aabbs)
    _tmins, _tmaxs, _hits = _ray_aabb_intersect(rays_o, rays_d, aabbs)
    assert torch.allclose(tmins, _tmins), (tmins - _tmins).abs().max()
    assert torch.allclose(tmaxs, _tmaxs), (tmaxs - _tmaxs).abs().max()
    assert (hits == _hits).all(), (hits == _hits).float().mean()

    # whether mid points are inside aabbs
    tmids = torch.clamp((tmins + tmaxs) / 2, min=0.0)
    points = tmids[:, :, None] * rays_d[:, None, :] + rays_o[:, None, :]
    _hits = (
        (points >= aabb_min[None, ...]) & (points <= aabb_max[None, ...])
    ).all(dim=-1)
    assert torch.allclose(hits, _hits)


@pytest.mark.skipif(not torch.cuda.is_available, reason="No CUDA device")
def test_traverse_grids():
    from nerfacc.grid import _enlarge_aabb, _query, traverse_grids

    torch.manual_seed(42)
    n_rays = 10
    n_aabbs = 4

    rays_o = torch.randn((n_rays, 3), device=device)
    rays_d = torch.randn((n_rays, 3), device=device)
    rays_d = rays_d / rays_d.norm(dim=-1, keepdim=True)

    base_aabb = torch.tensor([-1.0, -1.0, -1.0, 1.0, 1.0, 1.0], device=device)
    aabbs = torch.stack(
        [_enlarge_aabb(base_aabb, 2**i) for i in range(n_aabbs)]
    )

    binaries = torch.rand((n_aabbs, 32, 32, 32), device=device) > 0.5

    intervals, samples = traverse_grids(rays_o, rays_d, binaries, aabbs)

    ray_indices = samples.ray_indices
    t_starts = intervals.vals[intervals.is_left]
    t_ends = intervals.vals[intervals.is_right]
    positions = (
        rays_o[ray_indices]
        + rays_d[ray_indices] * (t_starts + t_ends)[:, None] / 2.0
    )
    occs, selector = _query(positions, binaries, base_aabb)
    assert occs.all(), occs.float().mean()
    assert selector.all(), selector.float().mean()


if __name__ == "__main__":
    test_ray_aabb_intersect()
    test_traverse_grids()
