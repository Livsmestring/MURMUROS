import { describe, it, expect } from 'vitest'
import { parseEnv } from './env.js'

describe('parseEnv', () => {
  it('returns defaults for an empty env', () => {
    const e = parseEnv({})
    expect(e.NODE_ENV).toBe('development')
    expect(e.PORT).toBe(3000)
    expect(e.LOG_LEVEL).toBe('info')
  })

  it('coerces PORT string to number', () => {
    expect(parseEnv({ PORT: '8080' }).PORT).toBe(8080)
  })

  it('accepts all valid NODE_ENV values', () => {
    for (const v of ['development', 'test', 'production'] as const) {
      expect(parseEnv({ NODE_ENV: v }).NODE_ENV).toBe(v)
    }
  })

  it('throws on unknown NODE_ENV', () => {
    expect(() => parseEnv({ NODE_ENV: 'staging' })).toThrow('Invalid environment variables')
  })

  it('throws on non-numeric PORT', () => {
    expect(() => parseEnv({ PORT: 'not-a-number' })).toThrow('Invalid environment variables')
  })

  it('accepts a valid DATABASE_URL', () => {
    const url = 'postgresql://localhost/murmuros'
    expect(parseEnv({ DATABASE_URL: url }).DATABASE_URL).toBe(url)
  })

  it('DATABASE_URL is undefined when not set', () => {
    expect(parseEnv({}).DATABASE_URL).toBeUndefined()
  })
})
