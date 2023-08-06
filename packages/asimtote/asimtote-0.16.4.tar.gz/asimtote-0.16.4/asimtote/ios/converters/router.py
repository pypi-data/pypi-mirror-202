# asimtote.ios.converters.router
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



import netaddr

from deepops import deepget

from ...diff import DiffConvert
from ..utils import VRF_GLOBAL



# --- converter classes ---



# =============================================================================
# ip[v6] route ...
# =============================================================================



class Cvt_IPRoute(DiffConvert):
    cmd = "ip-route", None, None, None

    def _cmd(self, vrf, net, r):
        n = netaddr.IPNetwork(net)

        return ("ip route"
                + ((" vrf " + vrf) if vrf else "")
                + " " + str(n.network) + " " + str(n.netmask)
                + ((" " + r["interface"]) if "interface" in r else "")
                + ((" " + r["router"]) if "router" in r else "")
                + ((" %d" % r["metric"]) if "metric" in r else "")
                + ((" tag %d" % r["tag"]) if "tag" in r else ""))

    def remove(self, old, vrf, net, id):
        return "no " + self._cmd(vrf, net, old)

    def update(self, old, upd, new, vrf, net, id):
        return self._cmd(vrf, net, new)


class Cvt_IPv6Route(DiffConvert):
    cmd = "ipv6-route", None, None, None

    def _cmd(self, vrf, net, r):
        return ("ipv6 route"
                + ((" vrf " + vrf) if vrf else "")
                + " " + net
                + ((" " + r["interface"]) if "interface" in r else "")
                + ((" " + r["router"]) if "router" in r else "")
                + ((" " + str(r["metric"])) if "metric" in r else "")
                + ((" tag " + str(r["tag"])) if "tag" in r else ""))

    def remove(self, old, vrf, net, id):
        return "no " + self._cmd(vrf, net, old)

    def update(self, old, upd, new, vrf, net, id):
        return self._cmd(vrf, net, new)



# =============================================================================
# route-map ...
# =============================================================================



class Cvt_RtMap(DiffConvert):
    cmd = "route-map", None
    block = "rtmap-del"

    def remove(self, old, rtmap):
        return "no route-map " + rtmap


class DiffConvert_RtMap(DiffConvert):
    context = Cvt_RtMap.cmd


class Cvt_RtMap_Entry(DiffConvert_RtMap):
    cmd = None,
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        return "no route-map %s %d" % (rtmap, seq)


class Cvt_RtMap_Entry_Action(DiffConvert_RtMap):
    cmd = None, "action"
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        return "route-map %s %s %d" % (rtmap, new, seq)


class DiffConvert_RtMap_Entry(DiffConvert_RtMap):
    context = DiffConvert_RtMap.context + Cvt_RtMap_Entry.cmd

    def enter(self, rtmap, rtmap_dict, seq):
        return ["route-map %s %s %d" % (rtmap, rtmap_dict["action"], seq)]


class Cvt_RtMap_MatchCmty_DelExact(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "community", "exact-match"
    block = "rtmap-del"
    trigger_blocks = { "rtmap-add-cmty" }

    # if removing the exact-match option, we need to clear the list and
    # recreate it without it
    def remove(self, old, rtmap, seq):
        if self.get_ext(old):
            l = self.enter(rtmap, old, seq)
            l.append(" no match community")
            return l


class DiffConvert_RtMap_MatchCmty(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "community", "communities", None


class Cvt_RtMap_MatchCmty_Del(DiffConvert_RtMap_MatchCmty):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq, cmty):
        l = self.enter(rtmap, old, seq)
        l.append(" no match community " + cmty)
        return l


class Cvt_RtMap_MatchCmty_add(DiffConvert_RtMap_MatchCmty):
    block = "rtmap-add-cmty"

    def update(self, old, upd, new, rtmap, seq, cmty):
        # TODO: need to handle applying 'exact-match' when list is the
        # same; will rework these to use split_args_offset to see if
        # that makes it easier (as we need the action from a higher
        # context but would like to set a lower context)
        l = self.enter(rtmap, new, seq)
        exact_match = deepget(new, "match", "community", "exact-match")
        l.append(" match community %s%s"
                     % (cmty, " exact-match" if exact_match else ""))
        return l

    def trigger(self, new, *args):
        return self.update(new, new, new, *args)


class Cvt_RtMap_MatchIPAddr(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ip-address"

class Cvt_RtMap_MatchIPAddr_Del(Cvt_RtMap_MatchIPAddr):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for addr in sorted(self.get_ext(rem)):
            l.append(" no match ip address " + addr)
        return l

class Cvt_RtMap_MatchIPAddr_Add(Cvt_RtMap_MatchIPAddr):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for addr in sorted(self.get_ext(upd)):
            l.append(" match ip address " + addr)
        return l


class Cvt_RtMap_MatchIPPfxLst(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ip-prefix-list"

class Cvt_RtMap_MatchIPPfxLst_Del(Cvt_RtMap_MatchIPPfxLst):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for pfx in sorted(self.get_ext(rem)):
            l.append(" no match ip address prefix-list " + pfx)
        return l

class Cvt_RtMap_MatchIPPfxLst_Add(Cvt_RtMap_MatchIPPfxLst):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for pfx in sorted(self.get_ext(upd)):
            l.append(" match ip address prefix-list " + pfx)
        return l


class Cvt_RtMap_MatchIPv6Addr(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ipv6-address"

class Cvt_RtMap_MatchIPv6Addr_Del(Cvt_RtMap_MatchIPv6Addr):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for addr in sorted(self.get_ext(rem)):
            l.append(" no match ipv6 address " + addr)
        return l

class Cvt_RtMap_MatchIPv6Addr_Add(Cvt_RtMap_MatchIPv6Addr):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for addr in sorted(self.get_ext(upd)):
            l.append(" match ipv6 address " + addr)
        return l


class Cvt_RtMap_MatchIPv6PfxLst(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ipv6-prefix-list"

class Cvt_RtMap_MatchIPv6PfxLst_Del(Cvt_RtMap_MatchIPv6PfxLst):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for pfx in sorted(self.get_ext(rem)):
            l.append(" no match ipv6 address prefix-list " + pfx)
        return l

class Cvt_RtMap_MatchIPv6PfxLst_Add(Cvt_RtMap_MatchIPv6PfxLst):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for pfx in sorted(self.get_ext(upd)):
            l.append(" match ipv6 address prefix-list " + pfx)
        return l


class Cvt_RtMap_MatchTag(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "tag"

class Cvt_RtMap_MatchTag_Del(Cvt_RtMap_MatchTag):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for tag in sorted(self.get_ext(rem)):
            l.append(" no match tag " + str(tag))
        return l

class Cvt_RtMap_MatchTag_Add(Cvt_RtMap_MatchTag):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for tag in sorted(self.get_ext(upd)):
            l.append(" match tag " + str(tag))
        return l


class Cvt_RtMap_SetCmty(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "community", "communities"

class Cvt_RtMap_SetCmty_Del(Cvt_RtMap_SetCmty):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for cmty in sorted(self.get_ext(rem)):
            l.append(" no set community " + cmty)
        return l

class Cvt_RtMap_SetCmty_Add(Cvt_RtMap_SetCmty):
    block = "rtmap-add"

    # TODO: need to handle case where list is the same but 'additive'
    # is only addition or removal
    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for cmty in sorted(self.get_ext(upd)):
            l.append(" set community "
                     + cmty
                     + (" additive" if "additive" in new["set"]["community"]
                            else ""))
        return l


class Cvt_RtMap_SetIPNxtHop(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop"

    def _cmd(self, nexthop):
        addr = nexthop["addr"]
        vrf = None
        if "vrf" in nexthop:
            vrf = ("vrf " + nexthop["vrf"]) if nexthop["vrf"] else "global"

        return "set ip" + ((" " + vrf) if vrf else "") + " next-hop " + addr

class Cvt_RtMap_SetIPNxtHop_Del(Cvt_RtMap_SetIPNxtHop):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        # we must remove all the 'set ip next-hop' commands individually
        l = self.enter(rtmap, old, seq)
        for nexthop in self.get_ext(old):
            l.append(" no " + self._cmd(nexthop))
        return l

class Cvt_RtMap_SetIPNxtHop_Add(Cvt_RtMap_SetIPNxtHop):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        # the 'set ip ... next-hop' commands are an ordered list and, if
        # anything has changed, we need to destroy the old one and
        # create the new one from scratch
        l = self.enter(rtmap, new, seq)
        if old:
            for old_nexthop in self.get_ext(old):
                l.append(" no " + self._cmd(old_nexthop))
        for new_nexthop in self.get_ext(new):
            l.append(" " + self._cmd(new_nexthop))
        return l


class Cvt_RtMap_SetIPNxtHopVrfy(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop-verify-availability"

    def remove(self, old, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        l.append(" no set ip next-hop verify-availability")
        return l

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        l.append(" set ip next-hop verify-availability")
        return l

class Cvt_RtMap_SetIPNxtHopVrfyTrk(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop-verify-availability-track", None

    def _cmd(self, seq, nexthop):
        return ("set ip next-hop verify-availability %s %s track %d"
                     % (nexthop["addr"], seq, nexthop["track-obj"]))

class Cvt_RtMap_SetIPNxtHopVrfy_Del(Cvt_RtMap_SetIPNxtHopVrfyTrk):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq, nexthop_seq):
        return self.enter(rtmap, old, seq) + [
                   " no "
                       + self._cmd(nexthop_seq,
                                   self.get_ext(old, nexthop_seq))]

class Cvt_RtMap_SetIPNxtHopVrfy_Add(Cvt_RtMap_SetIPNxtHopVrfyTrk):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq, nexthop_seq):
        # individual entries (ordered by sequence number) can be replaced but
        # the old entry must be removed first, before the new one added
        l = self.enter(rtmap, new, seq)
        if old:
            l.append(" no "
                     + self._cmd(nexthop_seq, self.get_ext(old, nexthop_seq)))
        l.append(" " + self._cmd(nexthop_seq, self.get_ext(new, nexthop_seq)))
        return l


class Cvt_RtMap_SetIPv6NxtHop(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ipv6-next-hop"

    def _cmd(self, nexthop):
        addr = nexthop["addr"]
        return "set ipv6 next-hop " + addr

class Cvt_RtMap_SetIPv6NxtHop_Del(Cvt_RtMap_SetIPv6NxtHop):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        # we must remove all the 'set ipv6 next-hop' commands individually
        l = self.enter(rtmap, old, seq)
        for nexthop in self.get_ext(old):
            l.append(" no " + self._cmd(nexthop))
        return l

class Cvt_RtMap_SetIPv6NxtHop_Add(Cvt_RtMap_SetIPv6NxtHop):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        # the 'set ip ... next-hop' commands are an ordered list and, if
        # anything has changed, we need to destroy the old one and
        # create the new one from scratch
        l = self.enter(rtmap, new, seq)
        if old:
            for old_nexthop in self.get_ext(old):
                l.append(" no " + self._cmd(old_nexthop))
        for new_nexthop in self.get_ext(new):
            l.append(" " + self._cmd(new_nexthop))
        return l


class Cvt_RtMap_SetLocalPref(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "local-preference"

class Cvt_RtMap_SetLocalPref_Del(Cvt_RtMap_SetLocalPref):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        return self.enter(rtmap, old, seq) + [" no set local-preference"]

class Cvt_RtMap_SetLocalPref_Add(Cvt_RtMap_SetLocalPref):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        return self.enter(rtmap, new, seq) + [
                   " set local-preference " + str(self.get_ext(new))]


class Cvt_RtMap_SetVRF(DiffConvert_RtMap_Entry):
    # this handles both 'set global' and 'set vrf ...'
    cmd = tuple()
    ext = "set", "vrf"

    def _cmd(self, entry):
        vrf = self.get_ext(entry)
        return "set " + (("vrf " + vrf) if vrf else "global")

class Cvt_RtMap_SetVRF_Del(Cvt_RtMap_SetVRF):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        return self.enter(rtmap, old, seq) + [" no " + self._cmd(old)]

class Cvt_RtMap_SetVRF_Add(Cvt_RtMap_SetVRF):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)

        # if there's a previous setting, and we're changing from global
        # to a VRF, or vice-versa, we need to clear the old setting
        # first
        if old and (bool(self.get_ext(old)) != bool(self.get_ext(new))):
            l.append(" no " + self._cmd(old))

        l.append(" " + self._cmd(new))
        return l



# =============================================================================
# router bgp ...
# =============================================================================



class Cvt_RtrBGP(DiffConvert):
    cmd = "router", "bgp", None

    def remove(self, old, asn):
        return "no router bgp " + str(asn)

    def add(self, new, asn):
        return "router bgp " + str(asn)


class DiffConvert_RtrBGP(DiffConvert):
    context = "router", "bgp", None

    def enter(self, asn):
        return ["router bgp " + str(asn)]


class Cvt_RtrBGP_BGPRtrID(DiffConvert_RtrBGP):
    cmd = "router-id",

    def remove(self, old, asn):
        return self.enter(asn) + [" no bgp router-id"]

    def update(self, old, upd, new, asn):
        return self.enter(asn) + [" bgp router-id " + new]


class Cvt_RtrBGP_Nbr(DiffConvert_RtrBGP):
    cmd = "neighbor", None

    def remove(self, old, *args):
        c, (nbr, ) = self.split_args(args)
        # when removing a neighbor that is a peer-group, we need to
        # state that
        return self.enter(*c) + [
                   "  no neighbor "
                       + nbr
                       + (" peer-group" if old.get("type") == "peer-group"
                              else "")]

    def add(self, new, *args):
        c, (nbr, ) = self.split_args(args)
        # we only explicitly need to add a neighbor if it's a peer-group
        # (normally, a neighbor is created implicitly by configuring
        # settings for it, starting by putting it in a peer-group or
        # its remote-as)
        if new.get("type") == "peer-group":
            return self.enter(*c) + ["  neighbor %s peer-group" % nbr]


class DiffConvert_RtrBGP_Nbr(DiffConvert_RtrBGP):
    context = DiffConvert_RtrBGP.context + Cvt_RtrBGP_Nbr.cmd

    # we're going to use these classes directly under the 'router,bgp,
    # ASN,neighbor,NBR' context and the 'router,bgp,ASN,vrf,VRF,
    # address-family,AF,neighbor,NBR' context but we also need access to
    # the NBR parameter for the commands (since they start 'neighbor
    # NBR ...')
    #
    # setting split_args_offset to -1 allows the use of split_args() to
    # get the variable-length context (excluding the NBR - the -1)
    # separately from the NBR+cmd+ext required by the methods
    split_args_offset = -1


class Cvt_RtrBGP_Nbr_FallOver(DiffConvert_RtrBGP_Nbr):
    cmd = "fall-over",

    def remove(self, old, *args):
        c, (nbr, ) = self.split_args(args)
        return self.enter(*c) + [" no neighbor %s fall-over" % nbr]

    def update(self, old, upd, new, *args):
        c, (nbr, ) = self.split_args(args)
        return self.enter(*c) + [
                   " neighbor %s fall-over %s"
                       % (nbr,
                          ("bfd " + new["bfd"]) if "bfd" in new
                               else "route-map " + new["route-map"])]


class Cvt_RtrBGP_Nbr_Pwd(DiffConvert_RtrBGP_Nbr):
    cmd = "password",

    def remove(self, old, *args):
        c, (nbr, ) = self.split_args(args)
        return self.enter(*c) + [" no neighbor %s password" % nbr]

    def update(self, old, upd, new, *args):
        c, (nbr, ) = self.split_args(args)
        return self.enter(*c) + [
                   " neighbor %s password %d %s"
                       % (nbr, new["encryption"], new["password"])]


class Cvt_RtrBGP_Nbr_PrGrpMbr(DiffConvert_RtrBGP_Nbr):
    # this converter is used to add or remove a neighbor to/from a
    # peer-group
    cmd = "peer-group",
    trigger_blocks = { "bgp-nbr-activate" }

    def remove(self, old, *args):
        c, (nbr, ) = self.split_args(args)
        return self.enter(*c) + ["  no neighbor %s peer-group %s" % (nbr, old)]

    def add(self, new, *args):
        c, (nbr, ) = self.split_args(args)
        return self.enter(*c) + ["  neighbor %s peer-group %s" % (nbr, new)]

    def update(self, old, upd, new, *args):
        c, (nbr, ) = self.split_args(args)
        return self.enter(*c) + [
                   "  no neighbor %s peer-group %s" % (nbr, old),
                   "  neighbor %s peer-group %s" % (nbr, new)]


class Cvt_RtrBGP_Nbr_RemAS(DiffConvert_RtrBGP_Nbr):
    cmd = "remote-as",

    # removing a remote AS actually removes the neighbor, so we deal
    # with that in the context, above - we just handle add/update here

    def update(self, old, upd, new, asn, nbr):
        return self.enter(asn) + [" neighbor %s remote-as %s" % (nbr, new)]


class Cvt_RtrBGP_Nbr_UpdSrc(DiffConvert_RtrBGP_Nbr):
    cmd = "update-source",

    def remove(self, old, asn, nbr):
        return self.enter(asn) + [" no neighbor %s update-source" % nbr]

    def update(self, old, upd,new, asn, nbr):
        return self.enter(asn) + [" neighbor %s update-source %s" % (nbr, new)]


# router bgp ... address-family ... [vrf ...]


# working out the address-family line is complicated and we do it in
# several places, so separate it into a function

def _RtrBGP_AF(vrf, af):
    # address families in the global routing table as in a VRF called
    # VRF_GLOBAL as a special case so everything lines up at the same
    # level in the inventory
    return (" address-family "
            + af
            + ((" vrf " + vrf) if vrf != VRF_GLOBAL else ""))


class Cvt_RtrBGP_AF(DiffConvert_RtrBGP):
    cmd = "vrf", None, "address-family", None

    def remove(self, old, asn, vrf, af):
        return self.enter(asn) + [" no" + _RtrBGP_AF(vrf, af)]

    def add(self, new, asn, vrf, af):
        return self.enter(asn) + [_RtrBGP_AF(vrf, af)]



class DiffConvert_RtrBGP_AF(DiffConvert_RtrBGP):
    context = DiffConvert_RtrBGP.context + Cvt_RtrBGP_AF.cmd

    def enter(self, asn, vrf, af):
        return super().enter(asn) + [_RtrBGP_AF(vrf, af)]


class Cvt_RtrBGP_AF_MaxPaths(DiffConvert_RtrBGP_AF):
    cmd = "maximum-paths",

    def remove(self, old, asn, vrf, af):
        return self.enter(asn, vrf, af) + ["  no maximum-paths %d" % old]

    def update(self, old, upd, new, asn, vrf, af):
        return self.enter(asn, vrf, af) + ["  maximum-paths %d" % new]


class Cvt_RtrBGP_AF_MaxPathsIBGP(DiffConvert_RtrBGP_AF):
    cmd = "maximum-paths-ibgp",

    def remove(self, old, asn, vrf, af):
        return self.enter(asn, vrf, af) + ["  no maximum-paths ibgp %d" % old]

    def update(self, old, upd, new, asn, vrf, af):
        return self.enter(asn, vrf, af) + ["  maximum-paths ibgp %d" % new]


# 'redistribute' is a single line command but operates more as a
# context and so is handled as one, although, unlike the 'neighbor ...'
# commands does not need to be handled different from global vs VRF
# address families, so we don't need two versions
#
# entering 'redistribute ...' will enable redistribution and 'no
# redistribute ...' will turn it off again
#
# configuring 'route-map' or 'metric' will turn these settings on, and
# enable redistribution at the same time (if it is not already)
#
# 'no redistribute ... route-map/metric' will turn them off, but leave
# redistribution itself on


# classes to cover the redistribution contexts


class Cvt_RtrBGP_AF_Redist_Simple(DiffConvert_RtrBGP_AF):
    cmd = "redistribute", { "static", "connected" }

    def remove(self, old, asn, vrf, af, proto):
        return self.enter(asn, vrf, af) + ["  no redistribute " + proto]

    def add(self, new, asn, vrf, af, proto):
        return self.enter(asn, vrf, af) + ["  redistribute " + proto]


class Cvt_RtrBGP_AF_Redist_OSPF(DiffConvert_RtrBGP_AF):
    cmd = "redistribute", { "ospf", "ospfv3" }, None

    def remove(self, old, asn, vrf, af, proto, proc):
        return (self.enter(asn, vrf, af)
                + ["  no redistribute %s %d" % (proto, proc)])

    def add(self, new, asn, vrf, af, proto, proc):
        return (self.enter(asn, vrf, af)
                + ["  redistribute %s %d" % (proto, proc)])


# context versions of above
#
# the parameter classes will be subclasses of these and use a variable
# length context split because the 'simple' protocols have no additional
# arguments but the OSPF one has a process number


class DiffConvert_RtrBGP_AF_Redist_Simple(DiffConvert_RtrBGP_AF):
    context = (
        DiffConvert_RtrBGP_AF.context + Cvt_RtrBGP_AF_Redist_Simple.cmd)

    # also get the protocol from the context
    split_args_offset = -1

    def _redist(self, proto):
        return "redistribute " + proto


class DiffConvert_RtrBGP_AF_Redist_OSPF(DiffConvert_RtrBGP_AF):
    context = (
        DiffConvert_RtrBGP_AF.context + Cvt_RtrBGP_AF_Redist_OSPF.cmd)

    # also get the protocol and process number from the context
    split_args_offset = -2

    def _redist(self, proto, proc):
        return "redistribute %s %d" % (proto, proc)


# redistribution parameter classes
#
# these have to use split_args() because the OSPF versions below use the
# same methods but have a different length context


class Cvt_RtrBGP_AF_Redist_Simple_Metric(DiffConvert_RtrBGP_AF_Redist_Simple):
    cmd = "metric",

    def remove(self, old, *args):
        c, redist = self.split_args(args)
        return self.enter(*c) + [
                   "  no %s metric" % self._redist(*redist)]

    def update(self, old, upd, new, *args):
        c, redist = self.split_args(args)
        return self.enter(*c) + [
                   "  %s metric %d" % (self._redist(*redist), new)]


class Cvt_RtrBGP_AF_Redist_Simple_RtMap(DiffConvert_RtrBGP_AF_Redist_Simple):
    cmd = "route-map",

    def remove(self, old, *args):
        c, redist = self.split_args(args)
        return self.enter(*c) + [
                   "  no %s route-map %s" % (self._redist(*redist), old)]

    def update(self, old, upd, new, *args):
        c, redist = self.split_args(args)
        return self.enter(*c) + [
                   "  %s route-map %s" % (self._redist(*redist), new)]


# OSPF version of the above parameter classes - these inherit from the
# OSPF context class, instead of the simple context class


class Cvt_RtrBGP_AF_Redist_OSPF_Metric(
    DiffConvert_RtrBGP_AF_Redist_OSPF, Cvt_RtrBGP_AF_Redist_Simple_Metric):

    pass


class Cvt_RtrBGP_AF_Redist_OSPF_RtMap(
    DiffConvert_RtrBGP_AF_Redist_OSPF, Cvt_RtrBGP_AF_Redist_Simple_RtMap):

    pass


# adding and removing entire neighbors as a context is only done in the
# non-global VRF (in the global VRF, neighbors are configured at the
# parent, 'router bgp' level and then only address-family specific
# parameters at that level; for VRFs, the whole neighbor, including the
# remote-as, is configured at the address-family level)

class Cvt_RtrBGP_AF_vrf_Nbr(DiffConvert_RtrBGP_AF, Cvt_RtrBGP_Nbr):
    def filter(self, asn, vrf, af, nbr):
        return vrf != VRF_GLOBAL



# this abstract class and the two that follow are used to create two
# versions of each command class below by inheriting from each
# separately - one for the global VRF and one for a different VRF
#
# this class modifies the path during construction in two different
# ways

class _DiffConvert_RtrBGP_AF_Nbr(DiffConvert_RtrBGP_AF):
    def __init__(self):
        self.add_nbr_path()
        super().__init__()

    def add_nbr_path(self):
        pass


# this class is for commands in the global VRF: the commands start with
# 'neighbor ...' but still operate in the [global] address-family
# context - as such, this just appends that to the 'cmd' attribute
#
# this is because commands in the global address-family do not add or
# delete entire neighbors (that's done at the 'router bgp' level), but
# just configured parameters about them

class DiffConvert_RtrBGP_AF_global_Nbr(_DiffConvert_RtrBGP_AF_Nbr):
    def add_nbr_path(self):
        self.cmd = ("neighbor", None) + self.cmd

    def filter(self, asn, vrf, *_):
        return vrf == VRF_GLOBAL


# on the other hand, this class is for commands in the non-global VRF:
# here the neighbor commands operate in a context of that neighbor,
# underneath the address-family - the context is extended by suffixing
# 'neighbor ...' onto it
#
# this is because, in a non-global VRF, neighbors are separate from
# those at the global level and must be created and can also be removed
# by removing the context, with 'no neighbor ...', rather than the
# individual parameters

class DiffConvert_RtrBGP_AF_vrf_Nbr(_DiffConvert_RtrBGP_AF_Nbr):
    def add_nbr_path(self):
        self.context = self.context + ("neighbor", None)

    def filter(self, asn, vrf, *_):
        return vrf != VRF_GLOBAL


# this is the global VRF version of 'neighbor ... activate'

class Cvt_RtrBGP_AF_global_Nbr_Act(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "activate",
    block = "bgp-nbr-activate"

    def remove(self, old, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + ["  no neighbor %s activate" % nbr]

    def update(self, old, upd, new, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + ["  neighbor %s activate" % nbr]


# this creates the non-global VRF version of 'neighbor ... activate'
#
# this pattern continues for all commands below that exist in both the
# global or non-global VRF

class Cvt_RtrBGP_AF_vrf_Nbr_Act(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_Act):

    pass


class Cvt_RtrBGP_AF_global_Nbr_AddPath(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "additional-paths",

    def _add_paths(self, p):
        return (
            " ".join([a for a in [ "send", "receive", "disable" ] if a in p]))

    def remove(self, old, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s additional-paths" % nbr]

    def truncate(self, old, rem, new, asn, vrf, af, nbr):
        # we can't remove types of additional-path, only provide a
        # complete new list
        return self.update(old, None, new, asn, vrf, af, nbr)

    def update(self, old, upd, new, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s additional-paths %s"
                       % (nbr, self._add_paths(new))]


class Cvt_RtrBGP_AF_global_Nbr_AdvAddPath(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "advertise-additional-paths", None

    def remove(self, old, asn, vrf, af, nbr, adv):
        # we can just remove any type and don't need to give the number
        # when removing 'best n'
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s advertise additional-paths %s"
                       % (nbr, adv)]

    def update(self, old, upd, new, asn, vrf, af, nbr, adv):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s advertise additional-paths %s"
                       % (nbr, ("best %d" % new) if adv == "best" else adv)]


# Cvt_RtrBGP_AF_vrf _Nbr_AdvAddPath
# does not exist - there is no non-global VRF version of this


class Cvt_RtrBGP_AF_global_Nbr_AlwAS(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "allowas-in",

    def truncate(self, old, rem, new, asn, vrf, af, nbr):
        # if we're truncating, we must be removing the 'max'
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s allowas-in" % nbr]

    def remove(self, old, asn, vrf, af, nbr):
        # removing the entire command
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s allowas-in" % nbr]

    def update(self, old, upd, new, asn, vrf, af, nbr):
        # either changing the 'max' or adding a plain form
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s allowas-in%s"
                       % (nbr, (" %d" % new["max"]) if "max" in new else "")]


class Cvt_RtrBGP_AF_vrf_Nbr_AlwAS(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_AlwAS):

    pass


# Cvt_RtrBGP_AF_global_Nbr_FallOver
# does not exist - there is no global VRF version of this (done at the
# 'router bgp' level)


class Cvt_RtrBGP_AF_vrf_Nbr_FallOver(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_Nbr_FallOver):

    pass


class Cvt_RtrBGP_AF_global_Nbr_FltLst(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "filter-list", None

    def remove(self, old, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s filter-list %d %s" % (nbr, old, dir_)]

    def update(self, old, upd, new, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s filter-list %d %s" % (nbr, new, dir_)]


class Cvt_RtrBGP_AF_vrf_Nbr_FltLst(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_FltLst):

    pass


class Cvt_RtrBGP_AF_global_Nbr_MaxPfx(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "maximum-prefix",

    def remove(self, old, asn, vrf, af, nbr):
        # oddly, when removing, the old maximum must be spefified but
        # not the threshold
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s maximum-prefix %d" % (nbr, old["max"])]

    def update(self, old, upd, new, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s maximum-prefix %d%s"
                       % (nbr,
                          new["max"],
                          (" %d" % new["threshold"]) if "threshold" in new
                               else "")]


class Cvt_RtrBGP_AF_vrf_Nbr_MaxPfx(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_MaxPfx):

    pass


class Cvt_RtrBGP_AF_global_Nbr_NHSelf(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "next-hop-self",

    def truncate(self, old, rem, new, asn, vrf, af, nbr):
        # if we're truncating, we must be changing to the plain form
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s next-hop-self" % nbr]

    def remove(self, old, asn, vrf, af, nbr):
        # removing the entire command
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s next-hop-self" % nbr]

    def update(self, old, upd, new, asn, vrf, af, nbr):
        # either updatring to 'all' or adding a plain form
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s next-hop-self%s"
                       % (nbr, " all" if new.get("all") else "")]


class Cvt_RtrBGP_AF_vrf_Nbr_NHSelf(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_NHSelf):

    pass


# Cvt_RtrBGP_AF_global_Nbr_Pwd
# does not exist - there is no global VRF version of this (done at the
# 'router bgp' level)


class Cvt_RtrBGP_AF_vrf_Nbr_Pwd(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_Nbr_Pwd):

    pass


# Cvt_RtrBGP_AF_global_Nbr_PrGrpMbr
# does not exist - there is no global VRF version of this (done at the
# 'router bgp' level)


class Cvt_RtrBGP_AF_vrf_Nbr_PrGrpMbr(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_Nbr_PrGrpMbr):

    pass


class Cvt_RtrBGP_AF_global_Nbr_PfxLst(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "prefix-list", None

    def remove(self, old, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s prefix-list %s %s" % (nbr, old, dir_)]

    def update(self, old, upd, new, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s prefix-list %s %s" % (nbr, new, dir_)]


class Cvt_RtrBGP_AF_vrf_Nbr_PfxLst(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_PfxLst):

    pass


class Cvt_RtrBGP_AF_vrf_Nbr_RemAS(DiffConvert_RtrBGP_AF_vrf_Nbr):
    cmd = "remote-as",

    def get_sort_key(self):
        # we need this to fire before we put peers into the group, so
        # make it run before everything else
        return "0_remote-as",

    def remove(self, old, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s remote-as" % nbr]

    def update(self, old, upd, new, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s remote-as %s" % (nbr, new)]


class Cvt_RtrBGP_AF_global_Nbr_RemPrivAS(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "remove-private-as",

    def truncate(self, old, rem, new, asn, vrf, af, nbr):
        # if we're truncating, we must be changing to the plain form
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s remove-private-as" % nbr]

    def remove(self, old, asn, vrf, af, nbr):
        # removing the entire command requires that 'all' is specified,
        # if it is enabled, otherwise nothing will be removed
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s remove-private-as%s"
                       % (nbr, " all" if old.get("all") else "")]

    def update(self, old, upd, new, asn, vrf, af, nbr):
        # either updatring to 'all' or adding a plain form
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s remove-private-as%s"
                       % (nbr, " all" if new.get("all") else "")]


class Cvt_RtrBGP_AF_vrf_Nbr_RemPrivAS(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_RemPrivAS):

    pass


class Cvt_RtrBGP_AF_global_Nbr_RtMap(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "route-map", None

    def remove(self, old, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s route-map %s %s" % (nbr, old, dir_)]

    def update(self, old, upd, new, asn, vrf, af, nbr, dir_):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s route-map %s %s" % (nbr, new, dir_)]


class Cvt_RtrBGP_AF_vrf_Nbr_RtMap(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_RtMap):

    pass


class Cvt_RtrBGP_AF_global_Nbr_SndCmty(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "send-community", None

    # the 'neighbor ... send-community' command is odd in that the
    # 'standard', 'extended' and 'both' options don't replace the
    # current setting but add or remove those communities to it
    #
    # the configuration is expressed as a set containing none, one or
    # both of 'standard' and 'extended'

    def remove(self, old, asn, vrf, af, nbr, cmty):
       return self.enter(asn, vrf, af) + [
                   "  no neighbor %s send-community %s" % (nbr, cmty)]

    def update(self, old, upd, new, asn, vrf, af, nbr, cmty):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s send-community %s" % (nbr, cmty)]


class Cvt_RtrBGP_AF_vrf_Nbr_SndCmty(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_SndCmty):

    pass


class Cvt_RtrBGP_AF_global_Nbr_SoftRecfg(DiffConvert_RtrBGP_AF_global_Nbr):
    cmd = "soft-reconfiguration",

    def remove(self, old, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  no neighbor %s soft-reconfiguration %s" % (nbr, old)]

    def update(self, old, upd, new, asn, vrf, af, nbr):
        return self.enter(asn, vrf, af) + [
                   "  neighbor %s soft-reconfiguration %s" % (nbr, new)]


class Cvt_RtrBGP_AF_vrf_Nbr_SoftRecfg(
    DiffConvert_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_SoftRecfg):

    pass



# router ospf ...
# =============================================================================



class Cvt_RtrOSPF(DiffConvert):
    cmd = "router", "ospf", None

    def remove(self, old, proc):
        return "no router ospf " + str(proc)

    def add(self, new, proc):
        return "router ospf " + str(proc)


class DiffConvert_RtrOSPF(DiffConvert):
    context = "router", "ospf", None

    def enter(self, proc):
        return ["router ospf " + str(proc)]


class Cvt_RtrOSPF_Id(DiffConvert_RtrOSPF):
    cmd = "id",

    def remove(self, old, proc):
        return self.enter(proc) + [" no router-id"]

    def update(self, old, upd, new, proc):
        return self.enter(proc) + [" router-id " + new]


class Cvt_RtrOSPF_AreaNSSA(DiffConvert_RtrOSPF):
    cmd = "area", None, "nssa"

    def remove(self, old, proc, area):
        return self.enter(proc) + [" no area %s nssa" % area]

    def truncate(self, old, upd, new, proc, area):
        # if we're truncating, we're removing options and we do that by
        # just re-entering the command without them, same as update()
        return self.update(old, None, new, proc, area)

    def update(self, old, upd, new, proc, area):
        s = ""
        if "no-redistribution" in new: s += " no-redistribution"
        if "no-summary" in new: s += " no-summary"
        return self.enter(proc) + [" area %s nssa%s" % (area, s)]


# passive-interface configuration is slightly odd as the default mode is
# stored (assuming it's not the default) and then a list of exceptions
# is maintained and it can go either way


class Cvt_RtrOSPF_PasvInt_Dflt(DiffConvert_RtrOSPF):
    cmd = "passive-interface", "default"

    def remove(self, old, proc):
        return self.enter(proc) + [" no passive-interface default"]

    def update(self, old, upd, new, proc):
        return self.enter(proc) + [" passive-interface default"]


# ... the exception interface lists must execute after changing the
# default mode, which they will do as 'default' comes before 'interface'
# and 'no-interface'

class Cvt_RtrOSPF_PasvInt_Int(DiffConvert_RtrOSPF):
    cmd = "passive-interface",
    ext = "interface", None

    def delete(self, old, rem, new, proc, int_name):
        # if we're changing the default mode, the old list of exceptions
        # will be removed by that, so we don't need to do it
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(proc) + [" no passive-interface " + int_name]

    def update(self, old, upd, new, proc, int_name):
        return self.enter(proc) + [" passive-interface " + int_name]


class Cvt_RtrOSPF_PasvInt_NoInt(DiffConvert_RtrOSPF):
    cmd = "passive-interface",
    ext = "no-interface", None

    def delete(self, old, rem, new, proc, int_name):
        # if we're changing the default mode, the old list of exceptions
        # will be removed by that, so we don't need to do it
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(proc) + [" passive-interface " + int_name]

    def update(self, old, upd, new, proc, int_name):
        return self.enter(proc) + [" no passive-interface " + int_name]



# =============================================================================
# router ospfv3 ...
# =============================================================================



class Cvt_RtrOSPFv3(DiffConvert):
    cmd = "router", "ospfv3", None

    def remove(self, old, proc):
        return "no router ospfv3 " + str(proc)

    def add(self, new, proc):
        return "router ospfv3 " + str(proc)


class DiffConvert_RtrOSPFv3(DiffConvert):
    context = "router", "ospfv3", None

    def enter(self, proc):
        return ["router ospfv3 " + str(proc)]


class Cvt_RtrOSPFv3_Id(DiffConvert_RtrOSPFv3):
    cmd = "id",

    def remove(self, old, proc):
        return self.enter(proc) + [" no router-id"]

    def update(self, old, upd, new, proc):
        return self.enter(proc) + [" router-id " + new]


class Cvt_RtrOSPFv3_AreaNSSA(DiffConvert_RtrOSPFv3):
    cmd = "area", None, "nssa"

    def remove(self, old, proc, area):
        return self.enter(proc) + [" no area %s nssa" % area]

    def truncate(self, old, upd, new, proc, area):
        # if we're truncating, we're removing options and we do that by
        # just re-entering the command without them, same as update()
        return self.update(old, None, new, proc, area)

    def update(self, old, upd, new, proc, area):
        s = ""
        if "no-redistribution" in new: s += " no-redistribution"
        if "no-summary" in new: s += " no-summary"
        return self.enter(proc) + [" area %s nssa%s" % (area, s)]


class Cvt_RtrOSPFv3_AF(DiffConvert_RtrOSPFv3):
    cmd = "address-family", None

    def remove(self, old, vrf, af):
        return self.enter(vrf) + [" no address-family " + af]

    def add(self, new, vrf, af):
        return self.enter(vrf) + [" address-family " + af]


class DiffConvert_RtrOSPFv3_AF(DiffConvert_RtrOSPFv3):
    context = DiffConvert_RtrOSPFv3.context + Cvt_RtrOSPFv3_AF.cmd

    def enter(self, vrf, af):
        return super().enter(vrf) + [" address-family " + af]


# see the Cvt_RtrOSPF_... versions above for the explanation of how
# these converters work


class Cvt_RtrOSPFv3_AF_PasvInt_Dflt(DiffConvert_RtrOSPFv3_AF):
    cmd = "passive-interface", "default"

    def remove(self, old, proc, af):
        return self.enter(proc, af) + [" no passive-interface default"]

    def update(self, old, upd, new, proc, af):
        return self.enter(proc, af) + [" passive-interface default"]


class Cvt_RtrOSPFv3_AF_PasvInt_Int(DiffConvert_RtrOSPFv3_AF):
    cmd = "passive-interface",
    ext = "interface", None

    def delete(self, old, rem, new, proc, af, int_name):
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(proc, af) + [" no passive-interface " + int_name]

    def update(self, old, upd, new, proc, af, int_name):
        return self.enter(proc, af) + [" passive-interface " + int_name]


class Cvt_RtrOSPFv3_AF_PasvInt_NoInt(DiffConvert_RtrOSPFv3_AF):
    cmd = "passive-interface",
    ext = "no-interface", None

    def delete(self, old, rem, new, proc, af, int_name):
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(proc, af) + [" passive-interface " + int_name]

    def update(self, old, upd, new, proc, af, int_name):
        return self.enter(proc, af) + [" no passive-interface " + int_name]
