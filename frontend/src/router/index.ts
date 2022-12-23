import { createRouter, createWebHistory, RouteRecordRaw, RouteRecord } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useUserStore } from '../stores/user'
import AuthLayout from '../layouts/AuthLayout.vue'
import AppLayout from '../layouts/AppLayout.vue'
import Page404Layout from '../layouts/Page404Layout.vue'
import axios from 'axios'

import RouteViewComponent from '../layouts/RouterBypass.vue'
import UIRoute from '../pages/admin/ui/route'

export interface INavigationRoute {
  name?: string
  path: string
  meta?: {
    nav?: {
      icon?: string
      displayName?: string
      disabled?: boolean
      hidden?: boolean
    }
    perms?: {
      requiresAuth?: boolean
      requiresStaff?: boolean
      requiresAdmin?: boolean
    }
  }
  redirect?: object
  component?: object
  children?: INavigationRoute[]
}

export const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: { name: 'dashboard' },
    meta: {
      nav: {
        icon: 'vuestic-iconset-dashboard',
        displayName: 'menu.activeStreams',
        disabled: true,
        hidden: true,
      },
      perms: {
        requiresAuth: false,
        requiresStaff: false,
        requiresAdmin: false,
      },
    },
  },
  {
    name: 'gsg',
    path: '/gsg',
    meta: {
      nav: {
        icon: 'vuestic-iconset-dashboard',
        displayName: 'menu.dashboard',
        disabled: false,
        hidden: false,
      },
      perms: {
        requiresAuth: true,
        requiresStaff: false,
        requiresAdmin: false,
      },
    },
    redirect: { name: 'dashboard' },
    component: AppLayout,
    children: [
      {
        name: 'dashboard',
        path: 'dashboard',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'menu.activeStreams',
            disabled: false,
            hidden: false,
          },
          perms: {
            requiresAuth: true,
            requiresStaff: false,
            requiresAdmin: false,
          },
        },
        component: () => import('../pages/gsg/ActiveStreams.vue'),
      },
      // UIRoute,
    ],
  },
  {
    name: 'self',
    path: '/self',
    meta: {
      nav: {
        icon: 'vuestic-iconset-dashboard',
        displayName: 'menu.selfservice',
        disabled: false,
        hidden: false,
      },
      perms: {
        requiresAuth: true,
        requiresStaff: false,
        requiresAdmin: false,
      },
    },
    redirect: { name: 'dashboard' },
    component: AppLayout,
    children: [
      {
        name: 'profile',
        path: '/self/profile/:service?',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'menu.profile',
            disabled: false,
            hidden: false,
          },
          perms: {
            requiresAuth: true,
            requiresStaff: false,
            requiresAdmin: false,
          },
        },
        component: () => import('../pages/gsg/self-service/Profile.vue'),
      },
      // UIRoute,
    ],
  },
  {
    name: 'staff',
    path: '/staff',
    meta: {
      nav: {
        icon: 'vuestic-iconset-dashboard',
        displayName: 'staff.staffArea',
        disabled: false,
        hidden: false,
      },
      perms: {
        requiresAuth: true,
        requiresStaff: true,
        requiresAdmin: false,
      },
    },
    redirect: { name: 'master-list' },
    component: AppLayout,
    children: [
      {
        name: 'master-list',
        path: 'master-list',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'staff.masterList',
            disabled: false,
            hidden: false,
          },
          perms: {
            requiresAuth: true,
            requiresStaff: true,
            requiresAdmin: false,
          },
        },
        component: () => import('../pages/gsg/staff/MasterList.vue'),
      },
      // UIRoute,
    ],
  },
  {
    path: '/auth',
    meta: {
      nav: {
        icon: 'vuestic-iconset-dashboard',
        displayName: 'menu.activeStreams',
        disabled: true,
        hidden: true,
      },
      perms: {
        requiresAuth: false,
        requiresStaff: false,
        requiresAdmin: false,
      },
    },
    component: AuthLayout,
    children: [
      {
        name: 'login',
        path: 'login_oauth',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'menu.activeStreams',
            disabled: true,
            hidden: false,
          },
          perms: {
            requiresAuth: false,
            requiresStaff: false,
            requiresAdmin: false,
          },
        },
        component: () => import('../pages/auth/login/LoginOAuth.vue'),
      },
      {
        name: 'validate_oauth',
        path: 'validate_oauth',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'menu.activeStreams',
            disabled: true,
            hidden: true,
          },
          perms: {
            requiresAuth: false,
            requiresStaff: false,
            requiresAdmin: false,
          },
        },
        component: () => import('../pages/auth/login/ValidateOAuth.vue'),
      },
      {
        path: '',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'menu.activeStreams',
            disabled: true,
            hidden: true,
          },
          perms: {
            requiresAuth: false,
            requiresStaff: false,
            requiresAdmin: false,
          },
        },
        redirect: { name: 'login' },
      },
    ],
  },
  {
    path: '/404',
    component: Page404Layout,
    meta: {
      nav: {
        icon: 'vuestic-iconset-dashboard',
        displayName: 'menu.activeStreams',
        disabled: true,
        hidden: true,
      },
      perms: {
        requiresAuth: false,
        requiresStaff: false,
        requiresAdmin: false,
      },
    },
    children: [
      {
        name: 'not-found-advanced',
        path: 'not-found-advanced',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'menu.activeStreams',
            disabled: true,
            hidden: true,
          },
          perms: {
            requiresAuth: false,
            requiresStaff: false,
            requiresAdmin: false,
          },
        },
        component: () => import('../pages/404-pages/VaPageNotFoundSearch.vue'),
      },
      {
        name: 'not-found-simple',
        path: 'not-found-simple',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'menu.activeStreams',
            disabled: true,
            hidden: true,
          },
          perms: {
            requiresAuth: false,
            requiresStaff: false,
            requiresAdmin: false,
          },
        },
        component: () => import('../pages/404-pages/VaPageNotFoundSimple.vue'),
      },
      {
        name: 'not-found-custom',
        path: 'not-found-custom',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'menu.activeStreams',
            disabled: true,
            hidden: true,
          },
          perms: {
            requiresAuth: false,
            requiresStaff: false,
            requiresAdmin: false,
          },
        },
        component: () => import('../pages/404-pages/VaPageNotFoundCustom.vue'),
      },
      {
        name: 'not-found-large-text',
        path: '/pages/not-found-large-text',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'menu.activeStreams',
            disabled: true,
            hidden: true,
          },
          perms: {
            requiresAuth: false,
            requiresStaff: false,
            requiresAdmin: false,
          },
        },
        component: () => import('../pages/404-pages/VaPageNotFoundLargeText.vue'),
      },
    ],
  },
  {
    path: '/overlay',
    component: AppLayout,
    meta: {
      nav: {
        icon: 'vuestic-iconset-dashboard',
        displayName: 'menu.overlays',
        disabled: true,
        hidden: true,
      },
      perms: {
        requiresAuth: false,
        requiresStaff: false,
        requiresAdmin: true,
      },
    },
    children: [
      {
        name: 'wombragen',
        path: '/overlay/wombragen',
        meta: {
          nav: {
            icon: 'vuestic-iconset-dashboard',
            displayName: 'menu.wombragen',
            disabled: true,
            hidden: true,
          },
          perms: {
            requiresAuth: false,
            requiresStaff: false,
            requiresAdmin: true,
          },
        },
        component: () => import('../pages/gsg/Wombragen.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  // mode: process.env.VUE_APP_ROUTER_MODE_HISTORY === 'true' ? 'history' : 'hash',
  routes,
})

router.beforeEach(async (to: any, from: any, next) => {
  const AuthStore = useAuthStore()
  const UserStore = useUserStore()

  if (AuthStore.accessToken !== '' && UserStore.self.isLoggedIn === true) {
    next()
    return
  }

  // instead of having to check every route record with
  // to.matched.some(record => record.meta.requiresAuth)
  if (to.meta.perms.requiresAuth) {
    if (AuthStore.accessToken !== '') {
      next()
      // next(await validateAndFetchRoute(to))
    } else {
      next('/auth/login_oauth')
    }
    return
    // this route requires auth, check if logged in
    // if not, redirect to login page.
  }
  next()
})

export const validateAndFetchRoute = async (route_path: any) => {
  const AuthStore = useAuthStore()
  const UserStore = useUserStore()

  const path = '/streamers/self'

  const axiosConfig = AuthStore.getAxiosConfig()

  try {
    const bearerResponse = await axios.get(path, axiosConfig)
    UserStore.$state.self = bearerResponse.data.self
  } catch (error: any) {
    if (error.response.status in [400, 401]) {
      const refresh_token = AuthStore.$state.refreshToken
      const refresh_path = '/token/refresh/'

      try {
        const refreshResponse = await axios.post(
          refresh_path,
          {
            refresh: refresh_token,
          },
          {
            baseURL: '/api',
            headers: {
              'Content-Type': 'application/json',
            },
          },
        )
        AuthStore.$state.accessToken = refreshResponse.data.access
        route_path = await validateAndFetchRoute(route_path)
      } catch (refreshError: any) {
        UserStore.$state.self = {
          username: '',
          isLoggedIn: false,
        }
        AuthStore.$state.refreshToken = ''
        AuthStore.$state.accessToken = ''
        route_path = {
          name: 'login',
          path: '/auth/login_oauth',
        } as RouteRecordRaw
      }
    } else if (error.response.status == 500) {
      UserStore.$state.self = {
        username: '',
        isLoggedIn: false,
      }
      AuthStore.$state.refreshToken = ''
      AuthStore.$state.accessToken = ''
      route_path = {
        name: 'login',
        path: '/auth/login_oauth',
      } as RouteRecordRaw
    }
  }
  return route_path
}

export default router
