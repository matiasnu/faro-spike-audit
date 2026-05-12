import { Component, OnInit, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Router, RouterOutlet, RouterLink, RouterLinkActive, NavigationEnd } from '@angular/router';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { Title } from '@angular/platform-browser';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private router = inject(Router);
  private announcer = inject(LiveAnnouncer);
  private titleService = inject(Title);
  private platformId = inject(PLATFORM_ID);

  ngOnInit(): void {
    if (!isPlatformBrowser(this.platformId)) return;

    this.router.events
      .pipe(filter(e => e instanceof NavigationEnd))
      .subscribe(() => {
        const pageTitle = this.titleService.getTitle();
        this.announcer.announce(`Navegaste a: ${pageTitle}`);

        // Mover foco al inicio del contenido principal tras cada navegación
        setTimeout(() => {
          const main = document.getElementById('main-content');
          if (main) {
            main.setAttribute('tabindex', '-1');
            main.focus({ preventScroll: false });
          }
        }, 100);
      });
  }
}
