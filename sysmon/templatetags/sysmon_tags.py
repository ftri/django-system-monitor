from collections import namedtuple
from django.contrib.humanize.templatetags.humanize import intcomma

from django import template

from psutil import AccessDenied


def bytes2human(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


register = template.Library()


def tofloat(value):
    try:
        return float(value)
    except ValueError:
        return 0

register.filter(name='tofloat', filter_func=tofloat)


class SysMon(template.Node):
    def render(self, context):
        context.update(self.build_context_dict())
        return ''

    @classmethod
    def build_context_dict(cls, static=False):
        context = {}
        try:
            import psutil as pu
        except:
            context['error_psutil'] = 'not_found'
            return context

        # cpu
        cpu_info = {
            'core': pu.cpu_count(),
            'used': intcomma(pu.cpu_percent(), use_l10n=False),
            }

        # memory
        mem_info = {
            'total': bytes2human(pu.virtual_memory().total),
            'used': intcomma(pu.virtual_memory().percent, use_l10n=False),
            }

        # disk
        partitions = list()
        for part in pu.disk_partitions():
            partitions.append({
                'device': part.device,
                'mountpoint': part.mountpoint,
                'fstype': part.fstype,
                'total': bytes2human(
                        pu.disk_usage(part.mountpoint).total),
                'percent': intcomma(pu.disk_usage(part.mountpoint).percent,
                                     use_l10n=False),
                })

        # network
        networks = list()
        for k, v in pu.net_io_counters(pernic=True).items():
            # Skip loopback interface
            if k == 'lo':
                continue

            networks.append({
                'device': k,
                'sent': bytes2human(v.bytes_sent),
                'recv': bytes2human(v.bytes_recv),
                'pkg_sent': v.packets_sent,
                'pkg_recv': v.packets_recv,
                })

        # processes
        processes = list()
        for process in pu.process_iter():

            try:
                percent = process.memory_percent()
            except AccessDenied:
                percent = "Access Denied"
            else:
                percent = int(percent)

            processes.append({
                'pid': process.pid,
                'name': process.name() if static else process.name,
                'status': process.status() if static else process.status,
                'user': process.username(),
                'memory': percent,
                # 'exe': process.exe(),
                'cpu_percent': process.cpu_percent(0.1) if static else process.cpu_percent
                })

        processes_sorted = sorted(
            processes, key=lambda p: p["memory"], reverse=True)

        context.update({
            'cpu_info': cpu_info,
            'mem_info': mem_info,
            'partitions': partitions,
            'networks': networks,
            'processes': processes_sorted[:10],
            })

        return context


@register.tag
def get_system_stats(parser, token):
    return SysMon()
